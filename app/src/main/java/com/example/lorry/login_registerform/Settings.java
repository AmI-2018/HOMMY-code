package com.example.lorry.login_registerform;

import android.annotation.TargetApi;
import android.graphics.Typeface;
import android.os.Build;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

public class Settings extends AppCompatActivity {

    private ImageView close;
    private TextView title, ip_text, port_text;
    private EditText[] ip = new EditText[4];
    private EditText port;
    private Button upgrade;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_settings);

        close = findViewById(R.id.close_settings);
        title = findViewById(R.id.settings_text);
        ip_text = findViewById(R.id.hub_ip_text);
        port_text = findViewById(R.id.port_text);
        ip[0] = findViewById(R.id.ip_1);
        ip[1] = findViewById(R.id.ip_2);
        ip[2] = findViewById(R.id.ip_3);
        ip[3] = findViewById(R.id.ip_4);
        port = findViewById(R.id.port_field);
        upgrade = findViewById(R.id.upgrade_button);

        Typeface custom_font = Typeface.createFromAsset(getAssets(), Constants.GUGI);
        title.setTypeface(custom_font);
        ip_text.setTypeface(custom_font);
        port_text.setTypeface(custom_font);

        close.setOnClickListener(v->finish());

        upgrade.setOnClickListener(v->{
            boolean empty = false;
            if (!(port.getText().toString().trim().length() > 0)){
                empty = true;
                Toast.makeText(getApplicationContext(), "Port Field is missing!",
                        Toast.LENGTH_SHORT).show();
            }
            for(int i =0 ; i<ip.length && !empty; i++){
                if(!(ip[i].getText().toString().trim().length() > 0)){
                    empty = true;
                    Toast.makeText(getApplicationContext(), (i+1)+"° IP field is missing!",
                            Toast.LENGTH_SHORT).show();
                }
            }
            if(!empty){
                boolean correct = true;
                for(EditText t : ip){
                    int tmp = Integer.valueOf(t.getText().toString());
                    if (tmp > 255 || tmp < 0)
                        correct= false;
                }
                if(correct){
                    String ipstr = buildIp();
                    if (!Constants.setBaseUrl(ipstr, Integer.valueOf(port.getText().toString()), getApplicationContext()))
                        Toast.makeText(getApplicationContext(), "Malformed IP address!",
                                Toast.LENGTH_SHORT).show();
                    else {
                        Toast.makeText(getApplicationContext(), "The Hub IP has been changed succesfully! ",
                                Toast.LENGTH_LONG).show();
                        finish();
                    }
                }
                else Toast.makeText(getApplicationContext(), "IP field takes int between 0 and 255!",
                        Toast.LENGTH_LONG).show();
            }
        });
    }

    private String buildIp(){
        String ipstr = ip[0].getText().toString().trim();
        for(int i =1 ; i < ip.length; i++)
            ipstr += " " + ip[i].getText().toString().trim();

        ipstr= ipstr.replace(" ", ".");
        return ipstr;
    }
}
