package com.example.lorry.login_registerform;

import android.content.Intent;
import android.os.Bundle;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class WelcomePage extends AppCompatActivity {

    private TextView welcome;
    private Button join, profile, logout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_page);

        if (PreferenceManager.getDefaultSharedPreferences(this).getString("username", "").isEmpty()) {
            startActivity(new Intent(this, MainActivity.class));
            finish();
        }

        welcome = findViewById(R.id.welcome_text);
        join = findViewById(R.id.join_button);
        profile = findViewById(R.id.profile_button);
        logout = findViewById(R.id.logout_button);

        welcome.setText("Ciao " + PreferenceManager.getDefaultSharedPreferences(this).getString("username", "")
                + "!");
        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                PreferenceManager.getDefaultSharedPreferences(getApplicationContext()).edit().remove("username").apply();
                startActivity(new Intent(getApplicationContext(), MainActivity.class));
                finish();
            }
        });
    }
}
