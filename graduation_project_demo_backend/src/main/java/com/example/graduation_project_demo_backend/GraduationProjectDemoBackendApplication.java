package com.example.graduation_project_demo_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@SpringBootApplication
public class GraduationProjectDemoBackendApplication {

	public static void main(String[] args) {
		prepareRecommenders();
		SpringApplication.run(GraduationProjectDemoBackendApplication.class, args);
	}

	private static void prepareRecommenders() {
		String[] command = { "/usr/bin/python3",
				"/Users/natsusaka/Desktop/graduation_project/graduation_project_demo_backend/recommenders/recommenders_prepare_model.py" };

		try {
			Process process = Runtime.getRuntime().exec(command);
			process.waitFor();

			BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(process.getInputStream()));

			String temp;
			while ((temp = bufferedReader.readLine()) != null)
				System.out.println(temp);

		} catch (Exception e) {
			System.exit(1);
		}
	}
}
