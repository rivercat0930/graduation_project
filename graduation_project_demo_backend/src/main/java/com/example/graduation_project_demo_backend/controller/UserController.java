package com.example.graduation_project_demo_backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.graduation_project_demo_backend.model.User;
import com.example.graduation_project_demo_backend.repo.UserRepo;

@RestController
@CrossOrigin("*")
@RequestMapping("/users")
public class UserController {
	@Autowired
	private UserRepo userRepo;

	@PostMapping("/new")
	public String addUser(@RequestBody User user) {
		try {
			userRepo.save(user);
			return "User added successfully!";
		} catch (Exception e) {
			return "Failed to add user: " + e.getMessage();
		}
	}
}
