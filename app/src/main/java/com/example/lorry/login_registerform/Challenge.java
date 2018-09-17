package com.example.lorry.login_registerform;

import android.content.Intent;
import android.graphics.Typeface;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class Challenge extends AppCompatActivity {

    private TextView challenge_text, description_text;
    private Button[] answers = new Button[4];
    private Button start;
    private ImageView image;
    private JSONObject current_challenge;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_challenge);

        image = findViewById(R.id.challenge_image);
        challenge_text = findViewById(R.id.challenge_text);
        description_text = findViewById(R.id.challenge_description);
        start = findViewById(R.id.start_challenge);
        answers[0] = findViewById(R.id.answer_a);
        answers[1] = findViewById(R.id.answer_b);
        answers[2] = findViewById(R.id.answer_c);
        answers[3] = findViewById(R.id.answer_d);

        try{
            current_challenge = new JSONObject(PreferenceManager.getDefaultSharedPreferences(getApplicationContext())
                    .getString("current_chal", ""));
            challenge_text.setText(current_challenge.getString("name"));
            Typeface custom_font = Typeface.createFromAsset(getAssets(), Constants.GUGI);
            challenge_text.setTypeface(custom_font);
            description_text.setText(getString(R.string.turn_text, current_challenge.getString("description")));
            findViewById(R.id.answer_layout1).setVisibility(View.GONE);
            findViewById(R.id.answer_layout2).setVisibility(View.GONE);
            switch(current_challenge.getInt("id")){
                case 1:
                    image.setImageResource(R.drawable.pulse);
                    break;
                case 2:
                    image.setImageResource(R.drawable.voice);
                    break;
                case 3:
                    image.setImageResource(R.drawable.dance);
                    break;
                case 4:
                    image.setImageResource(R.drawable.music_quiz);
                    break;
            }
        }catch (JSONException j){
            j.printStackTrace();
        }

        start.setOnClickListener(v->{
            try{
                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                        Constants.getStartChallenge() + current_challenge.getInt("id"),
                        null,
                        response->{
                                try {
                                    int id = current_challenge.getInt("id");
                                    switch (response.getInt("result")){
                                        case 1:
                                            //Starting activity
                                            Toast.makeText(getApplicationContext(), "CASE 1",
                                                    Toast.LENGTH_SHORT).show();
                                            switch (id){
                                                case 1:
                                                    start.setVisibility(View.GONE);
                                                    description_text.setText("Follow the instruction on the screen and...\nHold On!");
                                                    break;
                                                case 2:
                                                    Intent intent = new Intent(getApplicationContext(), VoiceHzChallenge.class);
                                                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                                    startActivity(intent);
                                                    break;
                                                case 3:
                                                    Intent intent1 = new Intent(getApplicationContext(), DanceStopChallenge.class);
                                                    intent1.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                                    startActivity(intent1);
                                                    break;
                                                case 4:
                                                    findViewById(R.id.answer_layout1).setVisibility(View.VISIBLE);
                                                    findViewById(R.id.answer_layout2).setVisibility(View.VISIBLE);
                                                    start.setVisibility(View.GONE);
                                                    break;
                                                default:
                                                    break;
                                            }
                                            break;
                                        case 2:
                                            //Starting activity
                                            Toast.makeText(getApplicationContext(), "CASE 2",
                                                    Toast.LENGTH_SHORT).show();
                                            switch (id){
                                                case 1:
                                                    start.setVisibility(View.GONE);
                                                    description_text.setText("Follow the instruction on the screen and...\nHold On!");
                                                    break;
                                                case 2:
                                                    Intent intent = new Intent(getApplicationContext(), VoiceHzChallenge.class);
                                                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                                    startActivity(intent);
                                                    break;
                                                case 3:
                                                    Intent intent1 = new Intent(getApplicationContext(), DanceStopChallenge.class);
                                                    intent1.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                                                    startActivity(intent1);
                                                    break;
                                                case 4:
                                                    findViewById(R.id.answer_layout1).setVisibility(View.VISIBLE);
                                                    findViewById(R.id.answer_layout2).setVisibility(View.VISIBLE);
                                                    start.setVisibility(View.GONE);
                                                    break;
                                                default:
                                                    break;
                                            }
                                            break;
                                        default:
                                            Toast.makeText(getApplicationContext(), "It's not your turn!",
                                                    Toast.LENGTH_SHORT).show();
                                            break;
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
            }catch (JSONException j){
                j.printStackTrace();
            }
        });

        for (int i = 0; i<4; i++){
            final int index = i;
            answers[i].setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    try{
                        char answer = (char)(index + ((int)'A'));
                        String api = current_challenge.getInt("id") + "/" + answer;
                        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                                Constants.getAnswerChallenge() + api,
                                null,
                                new Response.Listener<JSONObject>() {
                                    @Override
                                    public void onResponse(JSONObject response) {
                                        try {
                                            if(response.getString("result").equals("NOT AUTHORIZED")){
                                                Toast.makeText(getApplicationContext(), "It's not your turn!",
                                                        Toast.LENGTH_SHORT).show();
                                            }
                                            else if (response.getString("result").equals("WRONG")){
                                                findViewById(R.id.answer_layout1).setVisibility(View.INVISIBLE);
                                                findViewById(R.id.answer_layout2).setVisibility(View.INVISIBLE);
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
