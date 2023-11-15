package com.example.graduation_project_demo_backend.service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

import org.springframework.stereotype.Service;

@Service
public class SentimentAnaysisService {
	public boolean writeToFile() {
		try {
			// String command = "python3 ./for_recommend/test.py";
			// String command = "python3 ./for_recommend/user_location_reviews.py;
			String command[] = { "/usr/bin/python3",
					"/Users/natsusaka/Desktop/graduation_project/graduation_project_demo_backend/for_recommend/user_location_reviews.py" };

			ProcessBuilder processBuilder = new ProcessBuilder(command);
			processBuilder.redirectErrorStream(true); // 將錯誤流合併到輸出流

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
