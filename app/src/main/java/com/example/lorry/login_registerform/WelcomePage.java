package com.example.lorry.login_registerform;

import android.content.Intent;
import android.graphics.Typeface;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.lang.reflect.Method;
import java.util.HashMap;
import java.util.Map;

public class WelcomePage extends AppCompatActivity {

    private TextView welcome;
    private Button join, profile, logout;
    private JSONObject user_info;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_page);

        if (PreferenceManager.getDefaultSharedPreferences(this).getString("user_info", "").isEmpty()) {
            startActivity(new Intent(this, MainActivity.class));
            finish();
        }
        Typeface custom_font = Typeface.createFromAsset(getAssets(), "fonts/Gugi-Regular.ttf");
        welcome = findViewById(R.id.welcome_text);
        join = findViewById(R.id.join_button);
        join.setTypeface(custom_font);
        profile = findViewById(R.id.profile_button);
        profile.setTypeface(custom_font);
        logout = findViewById(R.id.logout_button);
        logout.setTypeface(custom_font);


        try{
            user_info = new JSONObject(PreferenceManager.getDefaultSharedPreferences(this).getString("user_info", ""));
            welcome.setText(getResources().getString(R.string.welcome, user_info.get("username").toString().toUpperCase()));
            welcome.setTypeface(custom_font);
        }catch (JSONException j){
            j.printStackTrace();
        }

        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).edit().remove("user_info").apply();
                startActivity(new Intent(getApplicationContext(), MainActivity.class));
                finish();
            }
        });

        join.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                try{
                    Map<String, String> map = new HashMap<>();
                    map.put("username", user_info.get("username").toString());
                    JSONObject json = new JSONObject(map);

                    JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                            Constants.JOIN_URL,
                            json,
                            new Response.Listener<JSONObject>() {
                                @Override
                                public void onResponse(JSONObject response) {
                                    try {
                                        if (response.getString("result").equals("SUCCESS")) {
                                            PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                                    .edit().putBoolean("admin", response.getBoolean("admin")).apply();
                                            Intent intent = new Intent(getApplicationContext(), Lobby.class);
                                            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                            startActivity(intent);
                                        } else if (response.getString("result").equals("LIMITE GIOCATORI RAGGIUNTO")){
                                            Toast.makeText(getApplicationContext(), "Limit players has been reached!",
                                                    Toast.LENGTH_SHORT).show();
                                        }
                                        else{
                                            Toast.makeText(getApplicationContext(), "Something went wrong! Try again",
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
                            });
                    RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
                    requestQueue.add(jsonObjectRequest);
                }catch (JSONException j){
                    j.printStackTrace();
                }
            }
        });

        profile.setOnClickListener(new View.OnClickListener(){
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), Profile.class));
            }
        });
    }
}
