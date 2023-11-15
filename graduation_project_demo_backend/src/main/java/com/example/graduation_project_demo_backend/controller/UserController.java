package com.example.graduation_project_demo_backend.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.graduation_project_demo_backend.model.User;
import com.example.graduation_project_demo_backend.repo.UserRepo;
import com.example.graduation_project_demo_backend.service.UserService;

@RestController
@CrossOrigin("*")
@RequestMapping("/users")
public class UserController {
	@Autowired
	private UserService userService;

	@Autowired
	private UserRepo userRepo;

	@GetMapping("/")
	public List<User> getUsers() {
		return userService.getAllUsers();
	}

	@PostMapping("/new")
	public String addUser(@RequestBody User user) {
		try {
			userService.newUser(user);
			return "User added successfully!";
		} catch (Exception e) {
			return "Failed to add user: " + e.getMessage();
		}
	}

	@DeleteMapping("/{id}")
	public ResponseEntity<String> deleteUser(@PathVariable Integer id) {
		userService.deleteUser(id);
		return ResponseEntity.ok("User deleted successfully!");
	}
}
