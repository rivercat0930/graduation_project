package com.example.graduation_project_demo_backend.service;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.graduation_project_demo_backend.model.User;
import com.example.graduation_project_demo_backend.repo.UserRepo;

import jakarta.transaction.Transactional;

@Service
public class UserService {
  @Autowired
  private UserRepo userRepo;

  @Transactional
  public List<User> getAllUsers() {
    return userRepo.findAll();
  }

  @Transactional
  public User newUser(User user) {
    userRepo.save(user);
    return user;
  }

  public void deleteUser(Integer id) {
    userRepo.deleteById(id);
  }
}
