package com.example.graduation_project_demo_backend.service;

import java.io.*;

import org.springframework.stereotype.Service;

@Service
public class SentimentAnaysisService {
	public boolean writeToFile() {
		try {
			String command = "python3 /Users/natsusaka/Desktop/graduation_project/graduation_project_demo_backend/for_recommend/user_location_reviews.py";
			Process process = Runtime.getRuntime().exec(command);
			System.out.println("Successssssss");
			int exitCode = process.waitFor();

			return exitCode == 0;
		} catch (IOException | InterruptedException e) {
			return false;
		}
	}
}
