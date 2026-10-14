package io.github.jd1378.otphelper

import io.github.jd1378.otphelper.utils.XiaomiHyperIslandHelper
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.junit.runners.JUnit4

@RunWith(JUnit4::class)
class XiaomiHyperIslandUnitTest {

  @Test
  fun testHyperIslandJson_uncopied() {
    val code = "849201"
    val jsonString = XiaomiHyperIslandHelper.buildHyperIslandJson(
        code = code,
        copied = false,
    )

    // Check size limit (3072 UTF-8 bytes)
    val utf8Bytes = jsonString.toByteArray(Charsets.UTF_8)
    assertTrue("JSON size must be <= 3072 bytes, was: ${utf8Bytes.size}", utf8Bytes.size <= 3072)

    val root = JSONObject(jsonString)
    assertTrue(root.has("param_v2"))
    val paramV2 = root.getJSONObject("param_v2")

    assertEquals(1, paramV2.getInt("protocol"))
    assertEquals(XiaomiHyperIslandHelper.DEFAULT_BUSINESS_CODE, paramV2.getString("business"))
    assertTrue(paramV2.getBoolean("updatable"))
    assertTrue(paramV2.getBoolean("islandFirstFloat"))
    assertFalse(paramV2.getBoolean("enableFloat"))
    assertEquals(3, paramV2.getInt("timeout"))

    // Drag-and-drop share data
    val island = paramV2.getJSONObject("param_island")
    assertEquals(1, island.getInt("islandProperty"))
    assertEquals(180, island.getInt("islandTimeout"))

    val shareData = island.getJSONObject("shareData")
    assertEquals(XiaomiHyperIslandHelper.ICON_KEY, shareData.getString("pic"))
    assertEquals(code, shareData.getString("content"))
    assertEquals(code, shareData.getString("shareContent"))

    // Big summary island (Official Template 2: Region A Image/Text 1 + Region B Text)
    val bigIsland = island.getJSONObject("bigIslandArea")
    val left = bigIsland.getJSONObject("imageTextInfoLeft")
    assertEquals(1, left.getInt("type"))
    assertEquals(XiaomiHyperIslandHelper.ICON_KEY, left.getJSONObject("picInfo").getString("pic"))
    assertEquals("OTP", left.getJSONObject("textInfo").getString("title"))
    assertEquals(code, bigIsland.getJSONObject("textInfo").getString("title"))

    // Small summary island (Official Template 1: Icon only)
    val smallIsland = island.getJSONObject("smallIslandArea")
    assertEquals(XiaomiHyperIslandHelper.ICON_KEY, smallIsland.getJSONObject("picInfo").getString("pic"))

    // Expanded state (Official Template 16: Verification code)
    val iconTextInfo = paramV2.getJSONObject("iconTextInfo")
    assertEquals(0, iconTextInfo.getJSONObject("animIconInfo").getInt("type"))
    assertEquals(XiaomiHyperIslandHelper.ICON_KEY, iconTextInfo.getJSONObject("animIconInfo").getString("src"))
    assertEquals(code, iconTextInfo.getString("title"))
    assertEquals("", iconTextInfo.getString("content"))
    assertFalse(iconTextInfo.has("subContent"))

    // Actions button (Button 1: Text button)
    val actions = paramV2.getJSONArray("actions")
    assertEquals(1, actions.length())
    val copyAction = actions.getJSONObject(0)
    assertEquals(2, copyAction.getInt("type"))
    assertEquals(XiaomiHyperIslandHelper.ACTION_COPY_KEY, copyAction.getString("action"))
    assertEquals("Copy", copyAction.getString("actionTitle"))
    assertTrue(copyAction.getBoolean("clickWithCollapse"))
  }

  @Test
  fun testHyperIslandJson_copied() {
    val code = "543210"
    val jsonString = XiaomiHyperIslandHelper.buildHyperIslandJson(
        code = code,
        copied = true,
    )

    val root = JSONObject(jsonString)
    val paramV2 = root.getJSONObject("param_v2")

    // On update after copying, no unsolicited auto-expansion
    assertFalse(paramV2.getBoolean("islandFirstFloat"))
    assertFalse(paramV2.getBoolean("enableFloat"))

    // shareContent remains intact for drag-and-drop
    val shareData = paramV2.getJSONObject("param_island").getJSONObject("shareData")
    assertEquals(code, shareData.getString("shareContent"))

    // Action title reflects copied state
    val copyAction = paramV2.getJSONArray("actions").getJSONObject(0)
    assertEquals("Copied", copyAction.getString("actionTitle"))
  }

  @Test
  fun testHyperIslandJson_conformsToOfficialValidator() {
    val jsonString =
        XiaomiHyperIslandHelper.buildHyperIslandJson(
            code = "998877",
            copied = false,
        )
    val tempFile = java.io.File.createTempFile("hyperisland_test", ".json")
    try {
      tempFile.writeText(jsonString)
      // When running in module app, root is ../
      val scriptPath =
          if (java.io.File("xiaomi-hyperisland/scripts/validate_payload.py").exists()) {
            "xiaomi-hyperisland/scripts/validate_payload.py"
          } else {
            "../xiaomi-hyperisland/scripts/validate_payload.py"
          }
      val process =
          ProcessBuilder(
              "python3",
              scriptPath,
              tempFile.absolutePath,
              "--big-template",
              "2",
              "--small-template",
              "1",
              "--expanded-template",
              "16",
              "--picture",
              XiaomiHyperIslandHelper.ICON_KEY,
              "--action",
              XiaomiHyperIslandHelper.ACTION_COPY_KEY,
          ).redirectErrorStream(true).start()
      val output = process.inputStream.bufferedReader().readText()
      val exitCode = process.waitFor()
      assertEquals("Validation failed with output:\n$output", 0, exitCode)
      assertTrue("Output should indicate passed checks: $output", output.contains("PASSED structural checks"))
    } finally {
      tempFile.delete()
    }
  }
}
