package Laba2;

import java.util.ArrayList;


public class Rashet {
    private float all_price = 0;
    private ArrayList <Float> order = new ArrayList<>();
    public void calculate(int number_of_portion, float price) {
        float discount = 0;
        for (int i = 1; i<=number_of_portion; i++){
            float totalprice = price;
            float total_discount_per_dishes = 0;
            if (i > 1){
                total_discount_per_dishes = price* i/100.f;
                discount+=total_discount_per_dishes;
            }
            totalprice -= total_discount_per_dishes;
            all_price+=totalprice;

        }
        order.add(discount);
    }

    public float getAll_price() {
        return all_price;
    }

    public ArrayList<Float> getOrder() {
        return order;
    }
}
