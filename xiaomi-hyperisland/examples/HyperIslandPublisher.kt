package com.example.hyperisland

import android.Manifest
import android.app.Notification
import android.app.NotificationChannel
import android.app.NotificationManager
import android.app.PendingIntent
import android.content.Context
import android.content.pm.PackageManager
import android.graphics.drawable.Icon
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import org.json.JSONObject

/**
 * OFFICIAL XIAOMI CONTRACT (client route): Android Notification with OEM extras.
 * Illustrative Kotlin integration, Android minSdk 26; compile within an Android app.
 * Requires your own ic_notification and ic_box resources in res/drawable.
 * The businessCode MUST match a Xiaomi-approved scenario, and an approved
 * official island template must be validated against the latest template library.
 *
 * Shows big summary template 2, small icon 1 and expanded template 10.
 * Requires a caller-supplied secure contentIntent for Track; without it the
 * plain Android notification is published instead of an incomplete island.
 * This sample was not compiled against an Android SDK or device-tested here.
 */
class HyperIslandPublisher(
    private val context: Context,
    private val businessCode: String,
    private val xiaomiSceneApproved: Boolean
) {
    private val manager: NotificationManager =
        context.getSystemService(NotificationManager::class.java)

    companion object {
        const val CHANNEL_ID = "live_package_status"
        private const val ICON_KEY = "miui.focus.pic_box"
        private const val PARAM_KEY = "miui.focus.param"
        private const val TRACK_ACTION_KEY = "miui.focus.action_track"
    }

    /** Create or update a package activity using the SAME stable notification ID. */
    fun publishPackage(
        notificationId: Int,
        status: String,
        body: String,
        compactText: String,
        contentIntent: PendingIntent? = null
    ): Boolean {
        ensureChannel()
        if (Build.VERSION.SDK_INT >= 33 &&
            context.checkSelfPermission(Manifest.permission.POST_NOTIFICATIONS) !=
            PackageManager.PERMISSION_GRANTED
        ) {
            // Caller should request the permission at an appropriate moment.
            return false
        }

        val builder = Notification.Builder(context, CHANNEL_ID)
            .setSmallIcon(R.drawable.ic_notification)
            .setContentTitle(status)
            .setContentText(body)
            .setContentIntent(contentIntent)
            .setCategory(Notification.CATEGORY_STATUS)
            .setOnlyAlertOnce(true)
            .setAutoCancel(false)

        if (xiaomiSceneApproved && businessCode.isNotBlank() && isHyperOS3() && contentIntent != null) {
            try {
                val json = createTemplateShapedJson(status, body, compactText)
                if (json.toByteArray(Charsets.UTF_8).size <= 3072) {
                    val pictures = Bundle().apply {
                        putParcelable(
                            ICON_KEY,
                            Icon.createWithResource(context, R.drawable.ic_box)
                        )
                    }
                    val action = Notification.Action.Builder(
                        Icon.createWithResource(context, R.drawable.ic_box),
                        "Track", contentIntent
                    ).build()
                    val actions = Bundle().apply { putParcelable(TRACK_ACTION_KEY, action) }
                    val xiaomiExtras = Bundle().apply {
                        putBundle("miui.focus.pics", pictures)
                        putBundle("miui.focus.actions", actions)
                        putString(PARAM_KEY, json)
                    }
                    builder.addExtras(xiaomiExtras)
                }
            } catch (_: Exception) {
                // Preserve the ordinary notification fallback if Xiaomi JSON fails.
            }
        }

        manager.notify(notificationId, builder.build())
        return true
    }

    /** Always close the live activity when its underlying task finishes. */
    fun finish(notificationId: Int) {
        manager.cancel(notificationId)
    }

    private fun ensureChannel() {
        val channel = NotificationChannel(
            CHANNEL_ID, "Package updates", NotificationManager.IMPORTANCE_DEFAULT
        )
        manager.createNotificationChannel(channel)
    }

    private fun isHyperOS3(): Boolean = try {
        Settings.System.getInt(
            context.contentResolver, "notification_focus_protocol", 0
        ) == 3
    } catch (_: Exception) {
        false
    }

    /**
     * Template-shaped demonstration, NOT a blanket guarantee that Xiaomi will
     * accept a business scene, shape, or arbitrary text width. Confirm against
     * the vendor's current template library and approved scene screenshots.
     */
    private fun createTemplateShapedJson(
        status: String, body: String, compactText: String
    ): String {
        val iconRef = JSONObject()
            .put("type", 1)
            .put("pic", ICON_KEY)
        val left = JSONObject()
            .put("type", 1)
            .put("picInfo", JSONObject(iconRef.toString()))
            .put("textInfo", JSONObject().put("title", "Parcel"))
        // Official big summary template 2: A image/text plus B text.
        val bigIsland = JSONObject()
            .put("imageTextInfoLeft", left)
            .put("textInfo", JSONObject().put("title", compactText))
        val smallIsland = JSONObject()
            .put("picInfo", JSONObject(iconRef.toString()))
        val island = JSONObject()
            .put("islandProperty", 1)
            .put("islandTimeout", 900) // seconds
            .put("bigIslandArea", bigIsland)
            .put("smallIslandArea", smallIsland)
        // Official expanded template 10: Text 2 + Recognition 1 + Button 3.
        val expanded = JSONObject()
            .put("type", 2)
            .put("title", status)
            .put("content", body)
        val hint = JSONObject()
            .put("type", 1)
            .put("title", "Track parcel")
            .put("content", "Details")
            .put("actionInfo", JSONObject().put("action", TRACK_ACTION_KEY))
        val paramV2 = JSONObject()
            .put("protocol", 1) // Xiaomi example field; NOT system protocol version
            .put("business", businessCode)
            .put("updatable", true)
            .put("islandFirstFloat", false)
            .put("enableFloat", false)
            .put("timeout", 30) // minutes; different from islandTimeout
            .put("aodTitle", status)
            .put("param_island", island)
            .put("baseInfo", expanded)
            .put("picInfo", JSONObject(iconRef.toString()))
            .put("hintInfo", hint)
        return JSONObject().put("param_v2", paramV2).toString()
    }
}

// Call with a stable ID across updates:
// val publisher = HyperIslandPublisher(context, approvedBusinessCode, xiaomiSceneApproved = true)
// publisher.publishPackage(2001, "Out for delivery", "Expected by 18:00", "Today", trackIntent)
// publisher.publishPackage(2001, "Delivered", "Parcel received", "Done", trackIntent)
// publisher.finish(2001)
