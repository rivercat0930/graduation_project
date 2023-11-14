package com.example.graduation_project_demo_backend.model;

import jakarta.persistence.*;
// @Data
@Entity
@Table(name = "users")
public class User {
	@Id
	@GeneratedValue(strategy = GenerationType.AUTO)
	@Column(name = "userid", unique = true, nullable = false, length = 50)
	private Integer uid;

	@Column(name = "username", nullable = true, length = 50)
	private String userName;
	
	@Column(name = "password", nullable = true, length = 50)
	private String password;

	public User() {
	}

	public User(Integer uid, String userName, String password) {
		this.uid = uid;
		this.userName = userName;
		this.password = password;
	}

	public Integer getUid() {
		return uid;
	}

	public void setUid(Integer uid) {
		this.uid = uid;
	}

	public String getUserName() {
		return userName;
	}

	public void setUserName(String userName) {
		this.userName = userName;
	}

	public String getPassword() {
		return password;
	}

	public void setPassword(String password) {
		this.password = password;
	}
}
