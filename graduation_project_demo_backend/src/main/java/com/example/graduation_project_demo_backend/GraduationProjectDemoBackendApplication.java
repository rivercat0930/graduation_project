package com.example.graduation_project_demo_backend;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.domain.EntityScan;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
@ComponentScan({"com.example.graduation_project_demo_backend","com.example.graduation_project_demo_backend.model","com.example.graduation_project_demo_backend.controller","com.example.graduation_project_demo_backend.service"})
@EntityScan({"com.example.graduation_project_demo_backend","com.example.graduation_project_demo_backend.model","com.example.graduation_project_demo_backend.controller","com.example.graduation_project_demo_backend.service"})
public class GraduationProjectDemoBackendApplication {

	public static void main(String[] args) {
		SpringApplication.run(GraduationProjectDemoBackendApplication.class, args);
	}

}
