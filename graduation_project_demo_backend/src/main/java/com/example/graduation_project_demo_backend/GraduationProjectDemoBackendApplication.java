package com.example.graduation_project_demo_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.BufferedReader;
import java.io.InputStreamReader;

@SpringBootApplication
public class GraduationProjectDemoBackendApplication {

	public static void main(String[] args) {
		// prepare recommenders
		prepareRecommenders();

		SpringApplication.run(GraduationProjectDemoBackendApplication.class, args);
	}

	/* This function will create a new process and run the python file to spawn
	 * a new recommend model. This model will store at the [project_root_dir]/recommenders ,
	 * and file name is []
	 *
	 * All else is just run a python file that it will prepare some files for next step task
	 * using
	 *
	 * WARNING: IF FILE CANNOT SPAWN AS RESULT AND IT WILL TERMINAL ALL SERVER.
	 */
	private static void prepareRecommenders() {
		String[] command = {"/bin/bash", "-c", "./recommenders/recommenders_prepare_model.py"};

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
