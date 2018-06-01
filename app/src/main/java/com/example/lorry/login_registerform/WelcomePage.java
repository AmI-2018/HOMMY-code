package com.example.lorry.login_registerform;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;

import org.w3c.dom.Text;

public class WelcomePage extends AppCompatActivity {

    private TextView welcome;
    private Button join,profile,logout;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_welcome_page);

        welcome = findViewById(R.id.welcome_text);
        join = findViewById(R.id.join_button);
        profile = findViewById(R.id.profile_button);
        logout = findViewById(R.id.logout_button);

        logout.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });
    }
}
