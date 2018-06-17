package com.example.lorry.login_registerform;

import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.json.JSONException;
import org.json.JSONObject;

public class Profile extends AppCompatActivity {

    TextView user;
    TextView birthDate;
    TextView genre;
    TextView won;
    TextView mpChallenge;
    Button back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        user = findViewById(R.id.id_text);
        birthDate = findViewById(R.id.birthdate_text);
        genre = findViewById(R.id.genre_text);
        won = findViewById(R.id.won_text);
        mpChallenge = findViewById(R.id.mpc_text);
        back = findViewById(R.id.profile_back_button);
       back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
        try {
            JSONObject tmp = new JSONObject(PreferenceManager.getDefaultSharedPreferences(this).getString("user_info", ""));
            ((TextView) findViewById(R.id.welcome_profile)).setText(getResources().getString(R.string.welcomeP,
                    tmp.get("username").toString()));
            user.setText(tmp.get("username").toString());
            String[] birth = tmp.get("birthDate").toString().split("\\s+");
            birthDate.setText(getResources().getString(R.string.birthdate_text, birth[1], birth[2], birth[3]));
            genre.setText(tmp.get("genre").toString());
            won.setText(tmp.get("challengeWon").toString());
            System.out.println(tmp.get("mostPlayedCat"));
            if (!tmp.get("mostPlayedCat").toString().equals("null"))
                mpChallenge.setText(tmp.get("mostPlayedCat").toString());
            else {
                /*mpChallenge.setVisibility(View.GONE);
                findViewById(R.id.mpc).setVisibility(View.GONE);*/
            }
        }
        catch(JSONException e) {
            e.printStackTrace();
        }
    }
}
