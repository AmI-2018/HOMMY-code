package com.example.lorry.login_registerform;

import android.content.Intent;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.EditText;
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

import java.util.HashMap;

public class MainActivity extends AppCompatActivity {

    private EditText user;
    private EditText psw;
    private CardView login;
    private TextView register;
    private CardView setting_button;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        user = findViewById(R.id.username);
        psw = findViewById(R.id.mpc_text);
        login = findViewById(R.id.login_card);
        register = findViewById(R.id.register_text);
        setting_button = findViewById(R.id.settings_button);

        register.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                startActivity(new Intent(getApplicationContext(), RegisterActivity.class));
            }
        });

        login.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                final String username = user.getText().toString().trim();
                final String password = psw.getText().toString().trim();
                if (username.isEmpty() || password.isEmpty()) {
                    Toast.makeText(getApplicationContext(), "Missing fields", Toast.LENGTH_SHORT).show();
                    return;
                }

                HashMap<String, String> map = new HashMap<>();
                map.put("username", username);
                map.put("psw", password);


                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                        Constants.getLoginUrl(),
                        new JSONObject(map),
                        new Response.Listener<JSONObject>() {
                            @Override
                            public void onResponse(JSONObject response) {
                                try {
                                    if (response.getInt("result") > 0) {
                                        PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                                .edit().putString("user_info", response.toString()).apply();
                                        Intent intent = new Intent(getApplicationContext(), WelcomePage.class);
                                        intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                        startActivity(intent);
                                    } else {
                                        Toast.makeText(getApplicationContext(), "Incorrect username or password",
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

                SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
                singletonRequest.addToRequestQueue(jsonObjectRequest);
            }
        });

        setting_button.setOnClickListener(v->{
            Intent intent = new Intent(getApplicationContext(), Settings.class);
            startActivity(intent);
        });
    }
}
