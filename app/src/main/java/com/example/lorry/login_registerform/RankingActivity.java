package com.example.lorry.login_registerform;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ListView;

import com.android.volley.Request;
import com.android.volley.toolbox.JsonObjectRequest;

import org.json.JSONArray;
import org.json.JSONException;

import java.util.LinkedList;
import java.util.List;

public class RankingActivity extends AppCompatActivity {

    private ListView[] best = new ListView[4];
    //private int[] resources = new int[4];
    Button back;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_ranking);

        best[0] = findViewById(R.id.list1);
        //resources[0] = R.id.list1;
        best[1] = findViewById(R.id.list2);
        //resources[1] = R.id.list2;
        best[2] = findViewById(R.id.list3);
        //resources[2] = R.id.list3;
        best[3] = findViewById(R.id.list4);
        //resources[3] = R.id.list4;

        back = findViewById(R.id.ranking_back_button);
        back.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                finish();
            }
        });

        for (int chal_id = 1; chal_id <= 4; chal_id++) {
            final int id = chal_id;
            //final int res = resources[id-1];
            ;
            JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.GET,
                    Constants.getRankingUrl() + chal_id,
                    null,
                    response -> {
                        try {
                            if (response.getString("result").equals("SUCCESS")) {
                                JSONArray j = response.getJSONArray("scores");
                                List<String> l = new LinkedList<>();
                                for (int i = 0; i < j.length(); i++)
                                    l.add(j.getString(i));
                                ArrayAdapter adapter = new ArrayAdapter(getApplicationContext(), android.R.layout.simple_expandable_list_item_1, l);
                                //CustomListAdapter adapter = new CustomListAdapter(RankingActivity.this, res, l);
                                best[id-1].setAdapter(adapter);
                            }
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    },
                    Exception::printStackTrace);
            SingletonRequest singletonRequest = SingletonRequest.getmInstance(getApplicationContext());
            singletonRequest.addToRequestQueue(jsonObjectRequest);
        }
    }
}
