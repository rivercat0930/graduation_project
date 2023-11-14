package com.example.graduation_project_demo_backend.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.example.graduation_project_demo_backend.service.SentimentAnaysisService;

import java.io.IOException;

@RestController
@CrossOrigin("*")
@RequestMapping("/sentimentAnalysis")
public class SentimentAnalysisController {
  @Autowired
  private SentimentAnaysisService sentimentAnalysisService;

  @PostMapping("/writefile")
  public String writeToFile() throws Exception, InterruptedException {
    try {
      sentimentAnalysisService.writeToFile();
      return "write success";
    } catch (Exception e) {
      return "write false:" + e.getMessage();
    }
  }

  @GetMapping("/test")
  public String test() throws Exception, InterruptedException {
    try {
      return "write success";
    } catch (Exception e) {
      return "write false:" ;
    }
  }
}
