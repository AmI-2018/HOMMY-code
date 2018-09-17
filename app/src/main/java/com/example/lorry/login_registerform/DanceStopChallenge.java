package com.example.lorry.login_registerform;

import android.content.Context;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.Handler;
import android.preference.PreferenceManager;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.CardView;
import android.util.Log;
import android.view.View;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONException;
import org.json.JSONObject;

import java.util.HashMap;
import java.util.Map;

public class DanceStopChallenge extends AppCompatActivity implements SensorEventListener{

    private CardView lose;
    private TextView text;
    private SensorManager mSensorManager;
    private Sensor mAccelerometer;

    private double initAcce=Double.NaN;
    private static final int GRACE=25;
    private int skips =GRACE;
    static public boolean isMusicOn=false;
    static public boolean active = true;
    private Listener listener;
    private final int id = 3;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_dance_stop_challenge);

        text = findViewById(R.id.dancetest);
        lose = findViewById(R.id.eliminationdance);
        lose.setVisibility(View.INVISIBLE);
        listener = ()-> {
            if (active){
                lose.setVisibility(View.VISIBLE);
                Map<String,Integer> map = new HashMap<>();
                map.put("id", this.id);

                JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST,
                        Constants.getNextChallenge(),
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
            }
            else stopGame();
        };

        mSensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        if (mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER) != null)
            mAccelerometer = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
        else
            throw new UnsupportedOperationException("No accelerometer hardware found");

        new Thread(()->{
            while(!isMusicOn);
            gameStart();
        }).start();
        //gameStart();
    }

    @Override
    public void onSensorChanged(SensorEvent sensorEvent) {
        if(isMusicOn) text.setText("MUSIC ON -> " + skips);
        else text.setText("MUSIC OFF -> " + skips);
        if(skips ==0){
            if(listener!=null)
            {
                stopGame();
                listener.lose();
            }
        }
        double mag=Math.sqrt(sensorEvent.values[0]*sensorEvent.values[0]+sensorEvent.values[1]*sensorEvent.values[1]+sensorEvent.values[2]*sensorEvent.values[2]);
        if(sensorEvent.sensor.getName().equals(mAccelerometer.getName()))
        {
            if(isMusicOn&&Math.abs(mag-initAcce)<0.1d)
                skips--;
            else if(!isMusicOn&&Math.abs(mag-initAcce)>0.4d)
                skips--;
            else
                skips =GRACE;

            initAcce=mag;
            Log.d("Accel",String.valueOf(initAcce));
        }

    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }
    public void gameStart(){
        mSensorManager.registerListener(DanceStopChallenge.this, mAccelerometer, SensorManager.SENSOR_DELAY_FASTEST);
        Toast.makeText(getApplicationContext(), "Registered",
                Toast.LENGTH_SHORT).show();
    }

    private void stopGame(){
        mSensorManager.unregisterListener(this);
    }

    public interface Listener{
        void lose();
    }
}
