package com.example.graduation_project_demo_backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;
import com.example.graduation_project_demo_backend.service.LocationCommentService;

@RestController
@CrossOrigin("*")
@RequestMapping("/locationComment")
public class LocationCommentController {
  @Autowired
  private LocationCommentService locationCommentService;

  @PostMapping("/writeLocationComment")
  public String getLocationComment() throws Exception, InterruptedException {
    try {
      locationCommentService.writeLocationNameToFile();
      locationCommentService.writeLocationCommentToFile();
      return "write success";
    } catch (Exception e) {
      return "write false:" + e.getMessage();
    }
  }
}
