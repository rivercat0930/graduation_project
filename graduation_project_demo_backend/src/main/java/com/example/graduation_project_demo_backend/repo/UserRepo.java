package com.example.graduation_project_demo_backend.repo;

import com.example.graduation_project_demo_backend.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

public interface UserRepo extends JpaRepository<User, Integer> {
  // void deleteUserByUid(Integer id);
  User findByUserName(String userName);
}
