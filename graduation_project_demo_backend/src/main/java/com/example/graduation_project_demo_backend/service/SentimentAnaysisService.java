package com.example.graduation_project_demo_backend.service;

import java.io.*;

public class SentimentAnaysisService {
	public boolean writeToFile() {
		try {
			String command = "python /Users/natsusaka/Desktop/cemotion_test/main.py ";
			Process process = Runtime.getRuntime().exec(command);
			int exitCode = process.waitFor();

			return exitCode == 0;
		} catch (IOException | InterruptedException e) {
			return false;
		}
	}
}
