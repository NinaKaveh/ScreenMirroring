package com.isep.screenmirroring;

import javax.imageio.ImageIO;
import javax.swing.*;
import java.awt.*;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;

public class Main {

    public static JFrame f = new JFrame();
    public static JPanel jPanel = new JPanel();
    public static JLabel picLabel = new JLabel();

    public static void main(String[] args) throws InterruptedException {

        //jPanel.addKeyListener(new MKeyListener());
        f.add(jPanel);
        //f.setExtendedState(JFrame.MAXIMIZED_BOTH);
        //f.setUndecorated(true);
        f.setVisible(true);
        Thread.sleep(1000);
        for (int i = 0; i < 1000000; i++) {
        try {

            Robot robot = new Robot();
            Rectangle area = new Rectangle(Toolkit.getDefaultToolkit().getScreenSize());

            BufferedImage Image = robot.createScreenCapture(area);
            displayImg(Image);
            //f.setUndecorated(false);
        } catch (AWTException e) {
            e.printStackTrace();
        }
        }
    }

    private static void displayImg(BufferedImage image) throws InterruptedException {

        picLabel.setIcon(new ImageIcon(image));
        jPanel.add(picLabel);

        Thread.sleep(1000/30);
    }
    /*static class MKeyListener extends KeyAdapter {

        @Override
        public void keyPressed(KeyEvent event) {

            char ch = event.getKeyChar();

            if (ch == 'a' || ch == 'b' || ch == 'c') {

                //System.out.println(event.getKeyChar());
                f.setUndecorated(false);

            }
        }}*/
        }
