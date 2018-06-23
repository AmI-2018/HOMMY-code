package com.example.lorry.login_registerform;

import android.content.Intent;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
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
import java.util.Map;

public class Challenge extends AppCompatActivity {

    private TextView challenge_text, description_text;
    private Button[] answers = new Button[4];
    private ImageView image;
    private JSONObject current_challenge;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_challenge);

        challenge_text = findViewById(R.id.challenge_text);
        description_text = findViewById(R.id.challenge_description);
        answers[0] = findViewById(R.id.answer_a);
        answers[1] = findViewById(R.id.answer_b);
        answers[2] = findViewById(R.id.answer_c);
        answers[3] = findViewById(R.id.answer_d);

        try{
            current_challenge = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                    .getString("current_chal", ""));
            challenge_text.setText(current_challenge.getString("name"));
            //description_text.setText(getString(R.string.trivia_description));
        }catch (JSONException j){
            j.printStackTrace();
        }


        for (int i = 0; i<4; i++){
            final int index = i;
            answers[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try{
                        char answer = (char)(index + ((int)'A'));
                        String api = current_challenge.getInt("id") + "/" + answer;
                        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                                Constants.ANSWER_CHALLENGE + api,
                                null,
                                new Response.Listener<JSONObject>() {
                                    @Override
                                    public void onResponse(JSONObject response) {
                                        try {
                                            if(response.getString("result").equals("NOT AUTHORIZED")){
                                                Toast.makeText(getApplicationContext(), "It's not your turn!",
                                                        Toast.LENGTH_SHORT).show();
                                            }
                                            else System.out.println(response.getString("result"));
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
                                })
                        {
                            /**
                             * Passing some request headers
                             */
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
                    }catch (JSONException j){
                        j.printStackTrace();
                    }
                }
            });
        }
    }
}
