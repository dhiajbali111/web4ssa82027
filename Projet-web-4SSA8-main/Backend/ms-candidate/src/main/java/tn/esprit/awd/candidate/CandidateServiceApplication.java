package tn.esprit.awd.candidate;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;

@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
public class CandidateServiceApplication {

    public static void main(String[] args) {
        org.springframework.boot.SpringApplication.run(CandidateServiceApplication.class, args);
    }
}
