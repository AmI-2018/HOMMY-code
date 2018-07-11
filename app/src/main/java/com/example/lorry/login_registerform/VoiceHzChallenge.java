package com.example.lorry.login_registerform;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Typeface;
import android.os.AsyncTask;
import android.preference.PreferenceManager;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.view.View;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.TimeUnit;

public class VoiceHzChallenge extends AppCompatActivity {
    final int REQUEST_PERMISSION_CODE = 1000;
    private TextView title, description;
    private ImageView image;
    private CardView card;
    private VoiceHzDetector challengeHandler;
    private Button repr_btn, continue_btn;
    private boolean start, tone;
    private final int id = 2;
    private int frequency_recorded;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_voice_hz_challenge);

        if(!checkPermissionFromDevice())
            requestPermission();

        start = tone = false;
        title = findViewById(R.id.voice_title);
        description = findViewById(R.id.voice_description);
        image = findViewById(R.id.voice_mic);
        card = findViewById(R.id.voice_rec);
        repr_btn = findViewById(R.id.reply_btn);
        continue_btn = findViewById(R.id.continue_btn);

        card.setVisibility(View.INVISIBLE);
        continue_btn.setVisibility(View.GONE);
        Typeface custom_font = Typeface.createFromAsset(getAssets(), Constants.GUGI);
        title.setTypeface(custom_font);

        image.setOnClickListener(v->{
            if (!tone)
                Toast.makeText(getApplicationContext(), "You should listen to the tone first!",
                        Toast.LENGTH_SHORT).show();
            else{
                start = true;
                description.setText("Recording...");
                card.setVisibility(View.VISIBLE);
                challengeHandler = new VoiceHzDetector();
                startRecording();
                image.setEnabled(false);
                repr_btn.setVisibility(View.GONE);
            }
        });

        repr_btn.setOnClickListener(v->{
            if(!start) {
                //HTTP Request to reproduce again the sound given by HOMMY
                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                        Constants.DO + id,
                        null,
                        response->{
                            try {
                                if (response.getString("result").equals("SUCCESS")){
                                    Toast.makeText(getApplicationContext(), "Success!",
                                            Toast.LENGTH_SHORT).show();
                                }
                                else {
                                    Toast.makeText(getApplicationContext(), "Something went wrong!",
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
                tone = true;
            }
            // Or Listen to your tone
            else challengeHandler.playTone();

        });

        continue_btn.setOnClickListener(v->{
            Map<String,Integer> map = new HashMap<>();
            map.put("frequency", frequency_recorded);
            map.put("id", this.id);

            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                    Constants.NEXT_CHALLENGE,
                    new JSONObject(map),
                    response->{
                        try {
                            if (response.getString("result").equals("INVALID CHALLENGE")){
                                Toast.makeText(getApplicationContext(), "INVALID CHALLENGE!",
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
            continue_btn.setVisibility(View.GONE);
        });
    }

    private void requestPermission() {
        ActivityCompat.requestPermissions(this,new String[]{
                Manifest.permission.RECORD_AUDIO
        },REQUEST_PERMISSION_CODE);
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        switch(requestCode){
            case REQUEST_PERMISSION_CODE:
                if(grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED)
                    Toast.makeText(getApplicationContext(), "Permission Granted",
                            Toast.LENGTH_SHORT).show();
                else
                    Toast.makeText(getApplicationContext(), "Permission Denied",
                            Toast.LENGTH_SHORT).show();
                break;
        }
    }

    private boolean checkPermissionFromDevice() {

        int record_audio_result = ContextCompat.checkSelfPermission(this, Manifest.permission.RECORD_AUDIO);
        return record_audio_result == PackageManager.PERMISSION_GRANTED;
    }

    private void startRecording(){

        new AsyncTask<Void,Void,Integer>(){

            @Override
            protected Integer doInBackground(Void... voids) {
                challengeHandler.startRecTone();
                try{
                    TimeUnit.SECONDS.sleep(5);
                    challengeHandler.stopRecTone();
                    TimeUnit.SECONDS.sleep(2);
                }catch(InterruptedException i){
                    i.printStackTrace();
                }
                return challengeHandler.analizeFrequency();
            }

            @Override
            protected void onPostExecute(Integer res) {
                super.onPostExecute(res);

                description.setText("Watch the result on the screen!");
                card.setVisibility(View.INVISIBLE);
                repr_btn.setVisibility(View.VISIBLE);
                repr_btn.setText("Your Tone");
                continue_btn.setVisibility(View.VISIBLE);
                frequency_recorded = res;
                Toast.makeText(getApplicationContext(), res.toString(),
                        Toast.LENGTH_SHORT).show();
            }
        }.execute();
    }
}
