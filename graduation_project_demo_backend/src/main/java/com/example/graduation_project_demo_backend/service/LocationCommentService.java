package com.example.graduation_project_demo_backend.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Service;

@Service
public class LocationCommentService {
  public boolean writeLocationNameToFile() {
    try {
      String command[] = { "/usr/bin/python3",
          "/Users/natsusaka/Desktop/graduation_project/graduation_project_demo_backend/location_comment/collect_location.py" };

      ProcessBuilder processBuilder = new ProcessBuilder(command);
      processBuilder.redirectErrorStream(true);

      Process process = processBuilder.start();
      BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));

      String line;
      while ((line = input.readLine()) != null) {
        System.out.println("===================\n" + line);
      }

      int exitCode = process.waitFor();
      return exitCode == 0;
    } catch (IOException | InterruptedException e) {
      e.printStackTrace();
      return false;
    }
  }

  public boolean writeLocationCommentToFile() {
    try {
      String command[] = { "/usr/bin/python3",
          "/Users/natsusaka/Desktop/graduation_project/graduation_project_demo_backend/location_comment/main.py" };

      ProcessBuilder processBuilder = new ProcessBuilder(command);
      processBuilder.redirectErrorStream(true);

      Process process = processBuilder.start();
      BufferedReader input = new BufferedReader(new InputStreamReader(process.getInputStream()));

      String line;
      while ((line = input.readLine()) != null) {
        System.out.println("===================\n" + line);
      }

      int exitCode = process.waitFor();
      return exitCode == 0;
    } catch (IOException | InterruptedException e) {
      e.printStackTrace();
      return false;
    }
  }
}
