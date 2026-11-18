package tn.esprit.awd.job.client;

import org.springframework.cloud.openfeign.FeignClient;
import org.springframework.web.bind.annotation.GetMapping;

import java.util.Map;

/** Placeholder Feign client — wired later for sync calls. */
@FeignClient(name = "ms-candidate", path = "/api/placeholder")
public interface RemotePingClient {

    @GetMapping("/ping")
    Map<String, String> ping();
}
