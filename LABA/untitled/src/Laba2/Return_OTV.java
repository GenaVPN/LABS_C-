package Laba2;

import javax.swing.*;
import java.awt.*;

public class Return_OTV extends JFrame {

    private String create_string(Dishes[] dis, Rashet ras){
        String str =String.format("<html>Стоимость обеда c учетом скидок: %.2fР <br>Скидки:", ras.getAll_price());
        int i = 0;
        for (Dishes dishes: dis){
            str= str.concat(String.format("<br>%s: %.2fР",dishes.getStr(),ras.getOrder().get(i++)));
        }
        return str;

    }

    Return_OTV(Dishes[] dis, Rashet ras){
        String str = create_string( dis, ras);
        setSize(new Dimension(200,180));
        setResizable(false);
        JLabel label = new JLabel(str);
        label.setVerticalAlignment(JLabel.CENTER);
        label.setBorder(BorderFactory.createEmptyBorder(5,5,5,5));
        add(label);
    }

}
