package io.github.jd1378.otphelper.utils

import android.app.Notification
import android.app.PendingIntent
import android.content.Context
import android.graphics.drawable.Icon
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.provider.Settings
import androidx.core.app.NotificationCompat
import io.github.jd1378.otphelper.R
import org.json.JSONArray
import org.json.JSONObject

/**
 * Xiaomi HyperOS 3 HyperIsland (Super Island) integration for OTP detection.
 *
 * Implements official HyperOS 3 templates:
 * - Big summary island: Template 2 (Region A Image/Text 1 + Region B Text)
 * - Small summary island: Template 1 (Icon only)
 * - Drag and drop: param_island.shareData with shareContent = detected OTP code
 * - Expanded state: Template 16 (New Icon/Text + Button 1 verification code template)
 */
object XiaomiHyperIslandHelper {
  const val ICON_KEY = "miui.focus.pic_code"
  const val ACTION_COPY_KEY = "miui.focus.action_copy"
  const val PARAM_KEY = "miui.focus.param"
  const val PICS_KEY = "miui.focus.pics"
  const val ACTIONS_KEY = "miui.focus.actions"
  const val DEFAULT_BUSINESS_CODE = "verification_code"

  /**
   * Checks whether the device manufacturer/brand belongs to Xiaomi (Xiaomi, Redmi, POCO).
   */
  fun isXiaomiDevice(): Boolean {
    val manufacturer = Build.MANUFACTURER.orEmpty()
    val brand = Build.BRAND.orEmpty()
    return manufacturer.equals("Xiaomi", ignoreCase = true) ||
        brand.equals("Xiaomi", ignoreCase = true) ||
        brand.equals("Redmi", ignoreCase = true) ||
        brand.equals("POCO", ignoreCase = true)
  }

  /**
   * Gated version query checking official HyperOS 3 protocol.
   */
  fun isHyperOS3(context: Context): Boolean =
      try {
        Settings.System.getInt(context.contentResolver, "notification_focus_protocol", 0) == 3
      } catch (_: Exception) {
        false
      }

  /**
   * Queries OEM provider focus display capability.
   */
  fun canShowFocus(context: Context): Boolean =
      try {
        val bundle = Bundle().apply { putString("package", context.packageName) }
        context.contentResolver.call(
            Uri.parse("content://miui.statusbar.notification.public"),
            "canShowFocus",
            null,
            bundle,
        )?.getBoolean("canShowFocus", false) ?: false
      } catch (_: Exception) {
        false
      }

  /**
   * Determines whether HyperIsland notification and pill should replace normal notification.
   */
  fun isHyperIslandSupported(context: Context): Boolean {
    return isXiaomiDevice() || isHyperOS3(context) || canShowFocus(context)
  }

  /**
   * Builds the official HyperOS 3 JSON envelope for verification code detection.
   */
  fun buildHyperIslandJson(
      context: Context? = null,
      code: String,
      copied: Boolean,
      businessCode: String = DEFAULT_BUSINESS_CODE,
      leftTitle: String =
          if (copied) {
            context?.getString(R.string.copied) ?: "Copied"
          } else {
            "OTP"
          },
      cardTitle: String = code,
      subContent: String? = null,
      actionTitle: String =
          if (copied) {
            context?.getString(R.string.copied) ?: "Copied"
          } else {
            context?.getString(R.string.copy) ?: "Copy"
          },
  ): String {

    val paramV2 =
        JSONObject().apply {
          put("protocol", 1)
          put("business", businessCode)
          put("updatable", true)
          put("islandFirstFloat", !copied)
          put("enableFloat", false)
          put("timeout", 3) // 3 minutes
          put("aodTitle", "$cardTitle: $code")

          val island =
              JSONObject().apply {
                put("islandProperty", 1)
                put("islandTimeout", 180) // 180 seconds

                // Drag and drop support:
                // User can drag from the pill to an input area to paste the code!
                val shareData =
                    JSONObject().apply {
                      put("pic", ICON_KEY)
                      put("title", cardTitle)
                      put("content", code)
                      put("shareContent", code)
                    }
                put("shareData", shareData)

                // Big Island Area (Official Summary Template 2: Region A Image/Text 1 + Region B Text)
                val bigIslandArea =
                    JSONObject().apply {
                      val left =
                          JSONObject().apply {
                            put("type", 1)
                            put(
                                "picInfo",
                                JSONObject().apply {
                                  put("type", 1)
                                  put("pic", ICON_KEY)
                                },
                            )
                            put(
                                "textInfo",
                                JSONObject().apply {
                                  put("title", leftTitle)
                                },
                            )
                          }
                      put("imageTextInfoLeft", left)
                      put(
                          "textInfo",
                          JSONObject().apply {
                            put("title", code)
                          },
                      )
                    }
                put("bigIslandArea", bigIslandArea)

                // Small Island Area (Official Summary Template 1: Icon only)
                val smallIslandArea =
                    JSONObject().apply {
                      put(
                          "picInfo",
                          JSONObject().apply {
                            put("type", 1)
                            put("pic", ICON_KEY)
                          },
                      )
                    }
                put("smallIslandArea", smallIslandArea)
              }
          put("param_island", island)

          val iconTextInfo =
              JSONObject().apply {
                put(
                    "animIconInfo",
                    JSONObject().apply {
                      put("type", 0)
                      put("src", ICON_KEY)
                    },
                )
                put("title", cardTitle)
                put("content", "")
                if (!subContent.isNullOrBlank()) {
                  put("subContent", subContent)
                }
              }
          put("iconTextInfo", iconTextInfo)

          // Button 1: actions array (Text button for Copy)
          val actionsArray =
              JSONArray().apply {
                put(
                    JSONObject().apply {
                      put("type", 2)
                      put("action", ACTION_COPY_KEY)
                      put("actionTitle", actionTitle)
                      put("clickWithCollapse", true)
                    },
                )
              }
          put("actions", actionsArray)
        }

    return JSONObject().put("param_v2", paramV2).toString()
  }

  /**
   * Attaches the HyperIsland JSON and associated picture/action bundles to the NotificationCompat.Builder.
   */
  fun attachHyperIslandExtras(
      context: Context,
      builder: NotificationCompat.Builder,
      code: String,
      copied: Boolean,
      copyPendingIntent: PendingIntent?,
  ): Boolean {
    if (copyPendingIntent == null) return false
    return try {
      val json = buildHyperIslandJson(context, code, copied)
      if (json.toByteArray(Charsets.UTF_8).size > 3072) {
        AppLogger.w("XiaomiHyperIslandHelper", "HyperIsland JSON exceeds 3072 bytes")
        return false
      }

      val iconRes = if (copied) R.drawable.baseline_check_24 else R.drawable.logo_round
      val pictures =
          Bundle().apply {
            putParcelable(
                ICON_KEY,
                Icon.createWithResource(context, iconRes),
            )
          }

      val copyAction =
          Notification.Action.Builder(
              Icon.createWithResource(
                  context,
                  if (copied) R.drawable.baseline_check_24 else R.drawable.baseline_content_copy_24,
              ),
              context.getString(if (copied) R.string.copied else R.string.copy),
              copyPendingIntent,
          ).build()

      val actions =
          Bundle().apply {
            putParcelable(ACTION_COPY_KEY, copyAction)
          }

      builder.addExtras(
          Bundle().apply {
            putString(PARAM_KEY, json)
            putBundle(PICS_KEY, pictures)
            putBundle(ACTIONS_KEY, actions)
          },
      )
      true
    } catch (e: Exception) {
      AppLogger.e("XiaomiHyperIslandHelper", "Failed to attach HyperIsland extras", e)
      false
    }
  }
}
