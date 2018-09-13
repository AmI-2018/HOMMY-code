package com.example.lorry.login_registerform;

import android.content.Intent;
import android.graphics.Typeface;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONException;
import org.json.JSONObject;

public class GameOverActivity extends AppCompatActivity {
    private TextView score,GO,YS;
    private Button new_game;
    private String name;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_game_over);

        Typeface custom_font = Typeface.createFromAsset(getAssets(), Constants.GUGI);

        score = findViewById(R.id.score);
        GO = findViewById(R.id.game_over);
        YS = findViewById(R.id.y_s);
        new_game = findViewById(R.id.button_Ng);

        try{
            JSONObject user_info = new JSONObject(PreferenceManager.getDefaultSharedPreferences(this).getString("user_info", ""));
            name = getResources().getString(R.string.welcome, user_info.get("username").toString().toUpperCase());
        }catch (JSONException j){
            j.printStackTrace();
        }

        GO.setTypeface(custom_font);
        YS.setTypeface(custom_font);

        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                Constants.getScoreUrl() + name,
                null,
                response->{
                    try {
                        if (response.getString("result").equals("SUCCESS")){
                            Toast.makeText(getApplicationContext(), "Success!",
                                    Toast.LENGTH_SHORT).show();
                            score.setText(response.getString("score"));
                        }
                        else {
                            Toast.makeText(getApplicationContext(), "Something went wrong!",
                                    Toast.LENGTH_SHORT).show();
                        }
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }
                },
                Exception::printStackTrace);

        score.setTypeface(custom_font);

        new_game.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent intent = new Intent(getApplicationContext(), WelcomePage.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                startActivity(intent);
            }
        });
    }
}
