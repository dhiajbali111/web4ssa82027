package tn.esprit.awd.interview;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class InterviewServiceApplication {

    public static void main(String[] args) {
        org.springframework.boot.SpringApplication.run(InterviewServiceApplication.class, args);
    }
}
