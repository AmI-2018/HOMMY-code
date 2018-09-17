package com.example.lorry.login_registerform;

import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.preference.PreferenceManager;
import android.support.v4.app.NotificationCompat;
import android.util.Log;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;
import com.google.firebase.messaging.FirebaseMessagingService;
import com.google.firebase.messaging.RemoteMessage;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class FcmMessagingService extends FirebaseMessagingService {

    @Override
    public void onMessageReceived(RemoteMessage remoteMessage) {
        String title = remoteMessage.getNotification().getTitle();
        /*String message = remoteMessage.getNotification().getBody();

        Intent intent = new Intent(this, WelcomePage.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
        PendingIntent pendingIntent = PendingIntent.getActivity(this,0, intent, PendingIntent.FLAG_ONE_SHOT);
        NotificationCompat.Builder builder = new NotificationCompat.Builder(this, "default");
        builder.setContentTitle(title);
        builder.setContentText(message);
        builder.setSmallIcon(R.mipmap.ic_launcher);
        builder.setAutoCancel(true);
        builder.setContentIntent(pendingIntent);
        NotificationManager notificationManager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        notificationManager.notify(0,builder.build());*/

        if(title.toLowerCase().equals("feedback")){
            Intent intent = new Intent(getApplicationContext(), Feedback.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
        }
        else if (title.toLowerCase().equals("gameover")){
            Intent intent = new Intent(getApplicationContext(), GameOverActivity.class);
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
            startActivity(intent);
        }
        else if (title.toLowerCase().equals("play"))
            DanceStopChallenge.isMusicOn=true;
        else if (title.toLowerCase().equals("stop"))
            DanceStopChallenge.isMusicOn=false;
        else if (title.toLowerCase().equals("dancestop"))
            DanceStopChallenge.active=false;
        else {
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                    Constants.getCurrentChallenge(),
                    null,
                    new Response.Listener<JSONObject>() {
                        @Override
                        public void onResponse(JSONObject response) {
                            try {
                                if (response.getInt("result") > 0) {
                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                            .edit().putString("current_categ", response.getString("type")).apply();
                                    PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                            .edit().putString("current_chal", response.toString()).apply();

                                    Intent intent2 = new Intent(getApplicationContext(), Challenge.class);
                                    intent2.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                    startActivity(intent2);
                                } else {
                                    Toast.makeText(getApplicationContext(), "Something went wrong! Try again later",
                                            Toast.LENGTH_SHORT).show();
                                }
                            } catch (JSONException e) {
                                e.printStackTrace();
                            }

                        }
                    },
                    new Response.ErrorListener() {
                        @Override
                        public void onErrorResponse(VolleyError error) {
                            error.printStackTrace();
                        }
                    }) {

                /**
                 * Passing some request headers
                 */
                @Override
                public Map<String, String> getHeaders() {
                    Map<String, String> headers = new HashMap<>();
                    try {
                        JSONObject user_info = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                .getString("user_info", ""));
                        headers.put("authorization", user_info.getString("username"));
                        return headers;
                    } catch (JSONException j) {
                        j.printStackTrace();
                    }

                    return headers;
                }
            };
            SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
            singletonRequest.addToRequestQueue(jsonObjectRequest);
        }
    }
}
