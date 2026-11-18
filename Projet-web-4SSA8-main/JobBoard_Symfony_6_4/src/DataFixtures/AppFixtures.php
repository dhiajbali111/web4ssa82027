<?php

declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\Application;
use App\Entity\Candidate;
use App\Entity\Company;
use App\Entity\Job;
use App\Entity\Skill;
use App\Entity\User;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

/**
 * Demo dataset for the teaching monolith (visible in UI + phpMyAdmin).
 * All accounts use password: password
 */
final class AppFixtures extends Fixture
{
    public function __construct(private UserPasswordHasherInterface $hasher)
    {
    }

    public function load(ObjectManager $manager): void
    {
        $makeUser = function (string $email, array $roles, string $first, string $last) use ($manager): User {
            $user = (new User())
                ->setEmail($email)
                ->setRoles($roles)
                ->setFirstName($first)
                ->setLastName($last);
            $user->setPassword($this->hasher->hashPassword($user, 'password'));
            $manager->persist($user);

            return $user;
        };

        // --- Skills catalog ---
        $skillNames = [
            'PHP', 'Symfony', 'Java', 'Spring Boot', 'REST', 'MySQL',
            'PostgreSQL', 'MongoDB', 'Docker', 'RabbitMQ', 'Angular',
            'React', 'Git', 'Linux', 'Microservices',
        ];
        /** @var array<string, Skill> $skills */
        $skills = [];
        foreach ($skillNames as $name) {
            $skill = (new Skill())->setName($name);
            $manager->persist($skill);
            $skills[$name] = $skill;
        }

        // --- Admin ---
        $makeUser('admin@jobboard.local', ['ROLE_ADMIN'], 'System', 'Admin');

        // --- Companies + recruiters ---
        $northstarOwner = $makeUser('recruiter@jobboard.local', ['ROLE_COMPANY'], 'Robin', 'Recruiter');
        $softhouseOwner = $makeUser('sara@softhouse.local', ['ROLE_COMPANY'], 'Sara', 'Ben Ali');
        $cloudOwner = $makeUser('karim@cloudnine.local', ['ROLE_COMPANY'], 'Karim', 'Trabelsi');

        $northstar = (new Company())
            ->setName('Northstar Digital')
            ->setCity('Tunis')
            ->setDescription('Product engineering studio focused on web platforms and APIs.')
            ->setOwner($northstarOwner);

        $softhouse = (new Company())
            ->setName('SoftHouse Tunisia')
            ->setCity('Sfax')
            ->setDescription('Software house delivering enterprise Java and Spring solutions.')
            ->setOwner($softhouseOwner);

        $cloudNine = (new Company())
            ->setName('CloudNine Labs')
            ->setCity('Sousse')
            ->setDescription('Cloud-native team building distributed systems and DevOps tooling.')
            ->setOwner($cloudOwner);

        $manager->persist($northstar);
        $manager->persist($softhouse);
        $manager->persist($cloudNine);

        // --- Candidates ---
        $caseyUser = $makeUser('candidate@jobboard.local', ['ROLE_CANDIDATE'], 'Casey', 'Candidate');
        $aminaUser = $makeUser('amina@student.local', ['ROLE_CANDIDATE'], 'Amina', 'Gharbi');
        $youssefUser = $makeUser('youssef@student.local', ['ROLE_CANDIDATE'], 'Youssef', 'Mansouri');
        $inesUser = $makeUser('ines@student.local', ['ROLE_CANDIDATE'], 'Ines', 'Khelifi');

        $casey = (new Candidate())
            ->setUser($caseyUser)
            ->setHeadline('Software Engineering Student — Symfony / PHP')
            ->setSummary('ESPRIT student interested in distributed web applications and clean architecture.');
        foreach (['PHP', 'Symfony', 'REST', 'MySQL', 'Git'] as $n) {
            $casey->addSkill($skills[$n]);
        }

        $amina = (new Candidate())
            ->setUser($aminaUser)
            ->setHeadline('Full-stack developer (Angular + Spring)')
            ->setSummary('Looking for a CDI or internship in Tunis. Strong on REST APIs and front-end.');
        foreach (['Java', 'Spring Boot', 'Angular', 'MySQL', 'Git'] as $n) {
            $amina->addSkill($skills[$n]);
        }

        $youssef = (new Candidate())
            ->setUser($youssefUser)
            ->setHeadline('Backend / microservices enthusiast')
            ->setSummary('Hands-on with Docker, messaging and service-oriented design.');
        foreach (['Java', 'Spring Boot', 'Docker', 'RabbitMQ', 'MongoDB', 'Microservices'] as $n) {
            $youssef->addSkill($skills[$n]);
        }

        $ines = (new Candidate())
            ->setUser($inesUser)
            ->setHeadline('React developer — open to remote')
            ->setSummary('Front-end focused, comfortable consuming REST APIs and working in agile teams.');
        foreach (['React', 'REST', 'Git', 'Linux'] as $n) {
            $ines->addSkill($skills[$n]);
        }

        $manager->persist($casey);
        $manager->persist($amina);
        $manager->persist($youssef);
        $manager->persist($ines);

        // --- Jobs (published + one draft) ---
        $jobSymfony = (new Job())
            ->setCompany($northstar)
            ->setTitle('Junior Symfony Developer')
            ->setDescription('Build and maintain Twig/Doctrine features for a recruitment platform. Mentoring included.')
            ->setContractType('INTERNSHIP')
            ->setLocation('Tunis')
            ->setRemote(true)
            ->setPublished(true);
        foreach (['PHP', 'Symfony', 'MySQL', 'Git'] as $n) {
            $jobSymfony->addSkill($skills[$n]);
        }

        $jobApi = (new Job())
            ->setCompany($northstar)
            ->setTitle('REST API Engineer')
            ->setDescription('Design REST endpoints, authentication and integration tests for partner mobile apps.')
            ->setContractType('CDI')
            ->setLocation('Tunis')
            ->setRemote(false)
            ->setPublished(true);
        foreach (['PHP', 'REST', 'MySQL', 'Docker'] as $n) {
            $jobApi->addSkill($skills[$n]);
        }

        $jobSpring = (new Job())
            ->setCompany($softhouse)
            ->setTitle('Spring Boot Backend Intern')
            ->setDescription('Join the candidature microservice team. JPA, Feign clients and PostgreSQL.')
            ->setContractType('INTERNSHIP')
            ->setLocation('Sfax')
            ->setRemote(false)
            ->setPublished(true);
        foreach (['Java', 'Spring Boot', 'PostgreSQL', 'REST'] as $n) {
            $jobSpring->addSkill($skills[$n]);
        }

        $jobMicro = (new Job())
            ->setCompany($cloudNine)
            ->setTitle('Microservices & Messaging Engineer')
            ->setDescription('Work on event-driven flows with RabbitMQ, Docker and Spring Cloud.')
            ->setContractType('CDD')
            ->setLocation('Sousse')
            ->setRemote(true)
            ->setPublished(true);
        foreach (['Java', 'Spring Boot', 'RabbitMQ', 'Docker', 'Microservices'] as $n) {
            $jobMicro->addSkill($skills[$n]);
        }

        $jobReact = (new Job())
            ->setCompany($cloudNine)
            ->setTitle('React Front-end Developer')
            ->setDescription('Ship SPA screens consuming the JobBoard API Gateway. Focus on UX and accessibility.')
            ->setContractType('FREELANCE')
            ->setLocation('Remote')
            ->setRemote(true)
            ->setPublished(true);
        foreach (['React', 'REST', 'Git'] as $n) {
            $jobReact->addSkill($skills[$n]);
        }

        $jobDraft = (new Job())
            ->setCompany($softhouse)
            ->setTitle('DevOps Engineer (draft)')
            ->setDescription('Draft offer — not visible on the public job list until published.')
            ->setContractType('CDI')
            ->setLocation('Sfax')
            ->setRemote(false)
            ->setPublished(false);
        foreach (['Docker', 'Linux', 'Git'] as $n) {
            $jobDraft->addSkill($skills[$n]);
        }

        foreach ([$jobSymfony, $jobApi, $jobSpring, $jobMicro, $jobReact, $jobDraft] as $job) {
            $manager->persist($job);
        }

        // --- Applications (different statuses for demos) ---
        $applications = [
            [$casey, $jobSymfony, 'SUBMITTED', 'I would love to contribute to the Symfony teaching monolith and learn Doctrine in depth.'],
            [$casey, $jobApi, 'UNDER_REVIEW', 'Experienced with REST conventions from university projects.'],
            [$amina, $jobSpring, 'INTERVIEW', 'Available for an interview next week. Spring Boot and Angular portfolio attached conceptually.'],
            [$amina, $jobApi, 'SUBMITTED', 'Interested in API design and OpenAPI documentation.'],
            [$youssef, $jobMicro, 'ACCEPTED', 'Built a small RabbitMQ demo for AWD Validation 1.'],
            [$youssef, $jobSpring, 'REJECTED', 'Strong backend profile; team already staffed for this intake.'],
            [$ines, $jobReact, 'SUBMITTED', 'Portfolio of React SPAs consuming REST APIs.'],
            [$ines, $jobSymfony, 'WITHDRAWN', 'Prefer front-end missions; withdrawing Symfony internship application.'],
        ];

        foreach ($applications as [$candidate, $job, $status, $letter]) {
            $application = (new Application())
                ->setCandidate($candidate)
                ->setJob($job)
                ->setStatus($status)
                ->setCoverLetter($letter);
            $manager->persist($application);
        }

        $manager->flush();
    }
}
