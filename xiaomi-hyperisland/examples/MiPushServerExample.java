package com.example.hyperisland.server;

import com.xiaomi.xmpush.server.Message;
import com.xiaomi.xmpush.server.Result;
import com.xiaomi.xmpush.server.Sender;

/**
 * OFFICIAL XIAOMI SERVER ROUTE - sample for a trusted Java backend, not Android.
 * Uses the Xiaomi MiPush server SDK API shown in Xiaomi's developer guide.
 *
 * Compile in your backend with the version of Xiaomi's approved MiPush SDK.
 * The MiPush APP_SECRET must come from a secure server-side secret store.
 * Payload must contain your approved business scenario and template fields.
 * This example was not compiled against a MiPush server SDK in this environment.
 */
public final class MiPushServerExample {
    private MiPushServerExample() {}

    /**
     * Create or update. Reuse notifyId for the same live activity; include
     * param_v2.orderId and increasing param_v2.sequence for real-time updates.
     */
    public static Result publish(
            String appSecret,
            String targetRegId,
            int stableNotifyId,
            String focusJson,
            String optionalPictureUrl
    ) throws Exception {
        if (focusJson.getBytes(java.nio.charset.StandardCharsets.UTF_8).length > 3072) {
            throw new IllegalArgumentException("miui.focus.param exceeds 3072 bytes");
        }

        Sender sender = new Sender(appSecret);
        Message.Builder builder = new Message.Builder()
                .title("Package status") // Standard notification fallback
                .description("See delivery progress")
                .notifyId(stableNotifyId)
                .extra("miui.focus.param", focusJson);

        if (optionalPictureUrl != null && !optionalPictureUrl.isBlank()) {
            if (!optionalPictureUrl.startsWith("https://")) {
                throw new IllegalArgumentException("MiPush pictures must be HTTPS");
            }
            builder.extra("miui.focus.pic_box", optionalPictureUrl);
        }

        Message message = builder.build();
        // Official Xiaomi example uses sender.send(message, regId, 3).
        return sender.send(message, targetRegId, 3);
    }

    /**
     * End a server-side island by submitting a matching approved payload with
     * param_v2.cancel=true, the same order / notify ID, and a new sequence.
     * Use publish(...) with that cancellation JSON payload.
     */
}
