package com.example.lorry.login_registerform;

import android.graphics.Typeface;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Feedback extends AppCompatActivity {

    private TextView feedback_text;
    private ImageView up,down;
    private int id_chal;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_feedback);

        feedback_text = findViewById(R.id.feedback_text);
        up = findViewById(R.id.thumbup);
        down = findViewById(R.id.thumbdown);

        try{
            JSONObject current_challenge = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                    .getString("current_chal", ""));
            id_chal = current_challenge.getInt("id");

        }catch (JSONException j){
            j.printStackTrace();
        }

        Typeface custom_font = Typeface.createFromAsset(getAssets(), Constants.GUGI);
        feedback_text.setTypeface(custom_font);

        up.setOnClickListener(v->{
            Map<String, Integer> map = new HashMap<>();
            map.put("rate", 1);
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                    Constants.FEEDBACK + id_chal,
                    new JSONObject(map),
                    response->{
                        try {
                            if (!response.getString("result").equals("SUCCESS")){
                                Toast.makeText(getApplicationContext(), "Something went Wrong!",
                                        Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    },
                    Exception::printStackTrace)
            {
                @Override
                public Map<String, String> getHeaders(){
                    Map<String, String> headers = new HashMap<>();
                    try{
                        JSONObject user_info = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                .getString("user_info", ""));
                        headers.put("authorization", user_info.getString("username"));
                        return headers;
                    }catch (JSONException j){
                        j.printStackTrace();
                    }
                    return headers;
                }
            };
            SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
            singletonRequest.addToRequestQueue(jsonObjectRequest);
            up.setVisibility(View.GONE);
            down.setVisibility(View.GONE);
            feedback_text.setText(getString(R.string.feedback_support));
        });

        down.setOnClickListener(v->{
            Map<String, Integer> map = new HashMap<>();
            map.put("rate", 0);
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                    Constants.FEEDBACK + id_chal,
                    new JSONObject(map),
                    response->{
                        try {
                            if (!response.getString("result").equals("SUCCESS")){
                                Toast.makeText(getApplicationContext(), "Something went Wrong!",
                                        Toast.LENGTH_SHORT).show();
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    },
                    Exception::printStackTrace)
            {
                @Override
                public Map<String, String> getHeaders(){
                    Map<String, String> headers = new HashMap<>();
                    try{
                        JSONObject user_info = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                                .getString("user_info", ""));
                        headers.put("authorization", user_info.getString("username"));
                        return headers;
                    }catch (JSONException j){
                        j.printStackTrace();
                    }
                    return headers;
                }
            };
            SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
            singletonRequest.addToRequestQueue(jsonObjectRequest);
            up.setVisibility(View.GONE);
            down.setVisibility(View.GONE);
            feedback_text.setText(getString(R.string.feedback_support));
        });
    }
}
