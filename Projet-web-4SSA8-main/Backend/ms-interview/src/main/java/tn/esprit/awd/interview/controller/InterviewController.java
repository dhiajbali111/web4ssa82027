package tn.esprit.awd.interview.controller;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/** Placeholder controller — exposes a ping endpoint only. */
@RestController
@RequestMapping("/api/placeholder")
public class InterviewController {

    @GetMapping("/ping")
    public Map<String, String> ping() {
        return Map.of("status", "ok", "service", "interview");
    }
}
