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

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_profile);

        TextView user = findViewById(R.id.ID);
        TextView birthDate = findViewById(R.id.date);
        TextView genre = findViewById(R.id.genre);
        TextView won = findViewById(R.id.won);
        TextView mpChallenge = findViewById(R.id.MpC);
        Button back = findViewById(R.id.profile_back_button);



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
            birthDate.setText(tmp.get("birthDate").toString());
            genre.setText(tmp.get("genre").toString());
            won.setText(tmp.get("challengeWon").toString());
            if (tmp.get("mostPlayedCat")!=null)
                mpChallenge.setText(tmp.get("mostPlayedCat").toString());
            else {
                mpChallenge.setVisibility(View.GONE);
                findViewById(R.id.MpC).setVisibility(View.GONE);
            }
        }
        catch(JSONException e) {
            e.printStackTrace();
        }
    }
}
