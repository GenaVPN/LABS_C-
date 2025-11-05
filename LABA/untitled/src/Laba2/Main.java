package Laba2;

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Main extends JFrame {
    //Объект класса для расчета чека
    public Rashet ras = new Rashet();
    private int number_bludo = 1;
    //Создал массив enum для удобного выбора блюда (Скорее задаток на будущее подключения базы данных)
    private Dishes[] dis = Dishes.values();
    private final int count_dishes = dis.length;
    private final JLabel main_label;
    private final JTextField order_text;
    private final JTextField price_text;
    private final JButton button;
    private final JLabel error_label;


    //Функция для переименования main_label
    private void rename() {
        String bludo = dis[number_bludo].getStr();
        String str = "Введите количество порций и цену 1 порции: " + bludo;
        main_label.setText(str);
    }

    //Сброс данных
    private void reset_data(){
        error_label.setText("");
        order_text.setText("");
        price_text.setText("");
        button.setText("Заказать");
        number_bludo = 0;
        rename();
        number_bludo++;
    }


    private void fun_button() {
        try {

            int order = Integer.parseInt(order_text.getText());
            float price_order = Float.parseFloat(price_text.getText());
            if (order > 100) {
                error_label.setText("Количество блюд не должно быть больше 100");
                return;
            }
            else if (order <0 || price_order<0) {
                error_label.setText("Числа меньше нуля, повторите попытку");
                return;
            }
            ras.calculate(order, price_order);
            if (number_bludo >= count_dishes) {

                JFrame otv = new Return_OTV(dis, ras);
                reset_data();
                ras = new Rashet();
                otv.setDefaultCloseOperation(JFrame.DISPOSE_ON_CLOSE);
                otv.setVisible(true);
                return;
            }
            error_label.setText("");
            order_text.setText("");
            price_text.setText("");

            rename();
            if (number_bludo == count_dishes - 1) {
                button.setText("Завершить");
            }
            number_bludo++;
        } catch (Exception ex) {
            error_label.setText("Некорректные данные, повторите попытку");
        }
    }

    public Main() {
        //редактирую JFrame
        setTitle("Меню");
        setLayout(new BorderLayout());

        //Константы и переменный
        int WIDTH = 450;
        int HEIGHT = 300;
        setSize(WIDTH, HEIGHT);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setResizable(false);

        // Основная панель
        JPanel main_panel = new JPanel(new BorderLayout(0, 10)); // Отступы между строками
        main_panel.setBorder(BorderFactory.createEmptyBorder(10, 10, 20, 10));

        //Текст с информацией, какое сейчас блюдо заказывается
        main_label = new JLabel("Введите количество порций и цену 1 порции: Борщ", SwingConstants.LEFT);


        //Панель с полями для введения данных
        JPanel center = new JPanel(new BorderLayout());

        JPanel jtext = new JPanel(new GridLayout(2, 2, 10, 15));
        jtext.setBorder(BorderFactory.createEmptyBorder(15,0,15,0));

        // Laybel для панели
        JLabel order_label = new JLabel("Кол-во порций:");
        JLabel price_label = new JLabel("Цена за 1 шт:");

        //Поля ввода
        order_text = new JTextField();
        price_text = new JTextField();
        order_text.setHorizontalAlignment(JTextField.CENTER);
        price_text.setHorizontalAlignment(JTextField.CENTER);

        // Кнопка
        JPanel buttonPanel = new JPanel(new FlowLayout());
        button = new JButton("Заказать");
        //добавил действие для кнопки
        button.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                fun_button();
            }
        });
        button.setPreferredSize(new Dimension(120, 40));
        buttonPanel.add(button);

        //Текст с ошибками
        JPanel error = new JPanel(new BorderLayout());
        error_label = new JLabel();
        error_label.setVerticalAlignment(JLabel.CENTER);
        error_label.setHorizontalAlignment(JLabel.CENTER);

        error.setPreferredSize(new Dimension(WIDTH, 30));
        error.add(error_label, BorderLayout.CENTER);

        //Добавление Элементов
        jtext.add(order_label);
        jtext.add(order_text);
        jtext.add(price_label);
        jtext.add(price_text);

        center.add(jtext, BorderLayout.CENTER);
        center.add(buttonPanel, BorderLayout.SOUTH);

        main_panel.add(main_label, BorderLayout.NORTH);
        main_panel.add(center, BorderLayout.CENTER);
        main_panel.add(error, BorderLayout.SOUTH);

        add(main_panel);
        setVisible(true);
    }


    public static void main(String[] args) {
        new Main();
    }
}