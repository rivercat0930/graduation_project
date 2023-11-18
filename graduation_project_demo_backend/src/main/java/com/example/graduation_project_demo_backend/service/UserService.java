package com.example.graduation_project_demo_backend.service;

import java.util.List;
import java.util.Optional;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.example.graduation_project_demo_backend.model.User;
import com.example.graduation_project_demo_backend.repo.UserRepo;

@Service
public class UserService {
  @Autowired
  private UserRepo userRepo;

  public List<User> getAllUsers() {
    return userRepo.findAll();
  }

  public User getUserbyId(Integer id) {
    // Long longId = Long.valueOf(id);
    Optional<User> optionalUser = userRepo.findById(id);
    return optionalUser.orElse(null);
  }

  public User newUser(User user) {
    userRepo.save(user);
    return user;
  }

  public User getUserByUserName(String userName) {
    return userRepo.findByUserName(userName);
  }

  public void deleteUser(Integer id) {
    userRepo.deleteById(id);
  }
}
