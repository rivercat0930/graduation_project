package com.example.graduation_project_demo_backend.repo;


import com.example.graduation_project_demo_backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserRepo extends JpaRepository<User, Integer> {
}
