package com.example.lorry.login_registerform;

import android.content.Intent;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

public class Lobby extends AppCompatActivity {

    private TextView text;
    private Button button;
    private boolean admin;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_lobby);

        admin = PreferenceManager.getDefaultSharedPreferences(this).getBoolean("admin", false);
        text = findViewById(R.id.lobby_text);
        button = findViewById(R.id.start_button);

        if(admin == true){
            text.setText(getResources().getString(R.string.lobby_text1));

            button.setOnClickListener(new View.OnClickListener() {
                @Override
                public void onClick(View v) {
                    Intent intent = new Intent(getApplicationContext(), Categories.class);
                    intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TASK);
                    startActivity(intent);
                    finish();
                }
            });
        }
        else{
            text.setText(getResources().getString(R.string.lobby_text2));
            button.setVisibility(View.GONE);
        }
    }
}
