#!/usr/bin/env python3
"""Pretty-format the minified Symfony JobBoard teaching monolith."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "JobBoard_Symfony_6_4" / "JobBoard_Symfony_6_4"


def w(rel: str, content: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.lstrip("\n").replace("\r\n", "\n"), encoding="utf-8")
    print(f"wrote {rel}")


# --- Entities ---
w(
    "src/Entity/User.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\UserRepository;
use Doctrine\ORM\Mapping as ORM;
use Symfony\Bridge\Doctrine\Validator\Constraints\UniqueEntity;
use Symfony\Component\Security\Core\User\PasswordAuthenticatedUserInterface;
use Symfony\Component\Security\Core\User\UserInterface;

#[ORM\Entity(repositoryClass: UserRepository::class)]
#[ORM\Table(name: 'app_user')]
#[UniqueEntity(fields: ['email'])]
class User implements UserInterface, PasswordAuthenticatedUserInterface
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 180, unique: true)]
    private string $email = '';

    #[ORM\Column]
    private array $roles = [];

    #[ORM\Column]
    private string $password = '';

    #[ORM\Column(length: 80)]
    private string $firstName = '';

    #[ORM\Column(length: 80)]
    private string $lastName = '';

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getEmail(): string
    {
        return $this->email;
    }

    public function setEmail(string $email): self
    {
        $this->email = strtolower($email);

        return $this;
    }

    public function getUserIdentifier(): string
    {
        return $this->email;
    }

    public function getRoles(): array
    {
        $roles = $this->roles;
        $roles[] = 'ROLE_USER';

        return array_values(array_unique($roles));
    }

    public function setRoles(array $roles): self
    {
        $this->roles = $roles;

        return $this;
    }

    public function getPassword(): string
    {
        return $this->password;
    }

    public function setPassword(string $password): self
    {
        $this->password = $password;

        return $this;
    }

    public function eraseCredentials(): void
    {
    }

    public function getFirstName(): string
    {
        return $this->firstName;
    }

    public function setFirstName(string $firstName): self
    {
        $this->firstName = $firstName;

        return $this;
    }

    public function getLastName(): string
    {
        return $this->lastName;
    }

    public function setLastName(string $lastName): self
    {
        $this->lastName = $lastName;

        return $this;
    }

    public function getFullName(): string
    {
        return trim($this->firstName.' '.$this->lastName);
    }
}
''',
)

w(
    "src/Entity/Skill.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\SkillRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: SkillRepository::class)]
class Skill
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 100, unique: true)]
    private string $name = '';

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function __toString(): string
    {
        return $this->name;
    }
}
''',
)

w(
    "src/Entity/Candidate.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\CandidateRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: CandidateRepository::class)]
class Candidate
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 150, nullable: true)]
    private ?string $headline = null;

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $summary = null;

    #[ORM\Column(length: 255, nullable: true)]
    private ?string $cvPath = null;

    #[ORM\OneToOne]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?User $user = null;

    /** @var Collection<int, Skill> */
    #[ORM\ManyToMany(targetEntity: Skill::class, cascade: ['persist'])]
    private Collection $skills;

    /** @var Collection<int, Application> */
    #[ORM\OneToMany(mappedBy: 'candidate', targetEntity: Application::class)]
    private Collection $applications;

    public function __construct()
    {
        $this->skills = new ArrayCollection();
        $this->applications = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getUser(): ?User
    {
        return $this->user;
    }

    public function setUser(User $user): self
    {
        $this->user = $user;

        return $this;
    }

    public function getHeadline(): ?string
    {
        return $this->headline;
    }

    public function setHeadline(?string $headline): self
    {
        $this->headline = $headline;

        return $this;
    }

    public function getSummary(): ?string
    {
        return $this->summary;
    }

    public function setSummary(?string $summary): self
    {
        $this->summary = $summary;

        return $this;
    }

    public function getCvPath(): ?string
    {
        return $this->cvPath;
    }

    public function setCvPath(?string $cvPath): self
    {
        $this->cvPath = $cvPath;

        return $this;
    }

    /** @return Collection<int, Skill> */
    public function getSkills(): Collection
    {
        return $this->skills;
    }

    public function addSkill(Skill $skill): self
    {
        if (!$this->skills->contains($skill)) {
            $this->skills->add($skill);
        }

        return $this;
    }

    /** @return Collection<int, Application> */
    public function getApplications(): Collection
    {
        return $this->applications;
    }
}
''',
)

w(
    "src/Entity/Company.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\CompanyRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: CompanyRepository::class)]
class Company
{
    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 150)]
    private string $name = '';

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $description = null;

    #[ORM\Column(length: 120, nullable: true)]
    private ?string $city = null;

    #[ORM\OneToOne]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?User $owner = null;

    /** @var Collection<int, Job> */
    #[ORM\OneToMany(mappedBy: 'company', targetEntity: Job::class, cascade: ['persist'], orphanRemoval: true)]
    private Collection $jobs;

    public function __construct()
    {
        $this->jobs = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getName(): string
    {
        return $this->name;
    }

    public function setName(string $name): self
    {
        $this->name = $name;

        return $this;
    }

    public function getDescription(): ?string
    {
        return $this->description;
    }

    public function setDescription(?string $description): self
    {
        $this->description = $description;

        return $this;
    }

    public function getCity(): ?string
    {
        return $this->city;
    }

    public function setCity(?string $city): self
    {
        $this->city = $city;

        return $this;
    }

    public function getOwner(): ?User
    {
        return $this->owner;
    }

    public function setOwner(User $owner): self
    {
        $this->owner = $owner;

        return $this;
    }

    /** @return Collection<int, Job> */
    public function getJobs(): Collection
    {
        return $this->jobs;
    }
}
''',
)

w(
    "src/Entity/Job.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\JobRepository;
use Doctrine\Common\Collections\ArrayCollection;
use Doctrine\Common\Collections\Collection;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: JobRepository::class)]
class Job
{
    public const CONTRACTS = ['CDI', 'CDD', 'INTERNSHIP', 'FREELANCE'];

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\Column(length: 180)]
    private string $title = '';

    #[ORM\Column(type: 'text')]
    private string $description = '';

    #[ORM\Column(length: 30)]
    private string $contractType = 'CDI';

    #[ORM\Column(length: 120, nullable: true)]
    private ?string $location = null;

    #[ORM\Column]
    private bool $remote = false;

    #[ORM\Column]
    private bool $published = false;

    #[ORM\Column]
    private \DateTimeImmutable $createdAt;

    #[ORM\ManyToOne(inversedBy: 'jobs')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Company $company = null;

    /** @var Collection<int, Skill> */
    #[ORM\ManyToMany(targetEntity: Skill::class, cascade: ['persist'])]
    private Collection $skills;

    /** @var Collection<int, Application> */
    #[ORM\OneToMany(mappedBy: 'job', targetEntity: Application::class)]
    private Collection $applications;

    public function __construct()
    {
        $this->createdAt = new \DateTimeImmutable();
        $this->skills = new ArrayCollection();
        $this->applications = new ArrayCollection();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getTitle(): string
    {
        return $this->title;
    }

    public function setTitle(string $title): self
    {
        $this->title = $title;

        return $this;
    }

    public function getDescription(): string
    {
        return $this->description;
    }

    public function setDescription(string $description): self
    {
        $this->description = $description;

        return $this;
    }

    public function getContractType(): string
    {
        return $this->contractType;
    }

    public function setContractType(string $contractType): self
    {
        $this->contractType = $contractType;

        return $this;
    }

    public function getLocation(): ?string
    {
        return $this->location;
    }

    public function setLocation(?string $location): self
    {
        $this->location = $location;

        return $this;
    }

    public function isRemote(): bool
    {
        return $this->remote;
    }

    public function setRemote(bool $remote): self
    {
        $this->remote = $remote;

        return $this;
    }

    public function isPublished(): bool
    {
        return $this->published;
    }

    public function setPublished(bool $published): self
    {
        $this->published = $published;

        return $this;
    }

    public function getCreatedAt(): \DateTimeImmutable
    {
        return $this->createdAt;
    }

    public function getCompany(): ?Company
    {
        return $this->company;
    }

    public function setCompany(Company $company): self
    {
        $this->company = $company;

        return $this;
    }

    /** @return Collection<int, Skill> */
    public function getSkills(): Collection
    {
        return $this->skills;
    }

    public function addSkill(Skill $skill): self
    {
        if (!$this->skills->contains($skill)) {
            $this->skills->add($skill);
        }

        return $this;
    }

    /** @return Collection<int, Application> */
    public function getApplications(): Collection
    {
        return $this->applications;
    }
}
''',
)

w(
    "src/Entity/Application.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Entity;

use App\Repository\ApplicationRepository;
use Doctrine\ORM\Mapping as ORM;

#[ORM\Entity(repositoryClass: ApplicationRepository::class)]
#[ORM\UniqueConstraint(name: 'candidate_job_unique', columns: ['candidate_id', 'job_id'])]
class Application
{
    public const STATUSES = ['SUBMITTED', 'UNDER_REVIEW', 'INTERVIEW', 'ACCEPTED', 'REJECTED', 'WITHDRAWN'];

    #[ORM\Id]
    #[ORM\GeneratedValue]
    #[ORM\Column]
    private ?int $id = null;

    #[ORM\ManyToOne(inversedBy: 'applications')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Candidate $candidate = null;

    #[ORM\ManyToOne(inversedBy: 'applications')]
    #[ORM\JoinColumn(nullable: false, onDelete: 'CASCADE')]
    private ?Job $job = null;

    #[ORM\Column(type: 'text', nullable: true)]
    private ?string $coverLetter = null;

    #[ORM\Column(length: 30)]
    private string $status = 'SUBMITTED';

    #[ORM\Column]
    private \DateTimeImmutable $submittedAt;

    public function __construct()
    {
        $this->submittedAt = new \DateTimeImmutable();
    }

    public function getId(): ?int
    {
        return $this->id;
    }

    public function getCandidate(): ?Candidate
    {
        return $this->candidate;
    }

    public function setCandidate(Candidate $candidate): self
    {
        $this->candidate = $candidate;

        return $this;
    }

    public function getJob(): ?Job
    {
        return $this->job;
    }

    public function setJob(Job $job): self
    {
        $this->job = $job;

        return $this;
    }

    public function getCoverLetter(): ?string
    {
        return $this->coverLetter;
    }

    public function setCoverLetter(?string $coverLetter): self
    {
        $this->coverLetter = $coverLetter;

        return $this;
    }

    public function getStatus(): string
    {
        return $this->status;
    }

    public function setStatus(string $status): self
    {
        $this->status = $status;

        return $this;
    }

    public function getSubmittedAt(): \DateTimeImmutable
    {
        return $this->submittedAt;
    }
}
''',
)

# --- Repositories ---
for name, entity in [
    ('UserRepository', 'User'),
    ('SkillRepository', 'Skill'),
    ('CandidateRepository', 'Candidate'),
    ('CompanyRepository', 'Company'),
    ('ApplicationRepository', 'Application'),
]:
    w(
        f"src/Repository/{name}.php",
        f'''
<?php

declare(strict_types=1);

namespace App\\Repository;

use App\\Entity\\{entity};
use Doctrine\\Bundle\\DoctrineBundle\\Repository\\ServiceEntityRepository;
use Doctrine\\Persistence\\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<{entity}>
 */
final class {name} extends ServiceEntityRepository
{{
    public function __construct(ManagerRegistry $registry)
    {{
        parent::__construct($registry, {entity}::class);
    }}
}}
''',
    )

w(
    "src/Repository/JobRepository.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Repository;

use App\Entity\Job;
use Doctrine\Bundle\DoctrineBundle\Repository\ServiceEntityRepository;
use Doctrine\Persistence\ManagerRegistry;

/**
 * @extends ServiceEntityRepository<Job>
 */
final class JobRepository extends ServiceEntityRepository
{
    public function __construct(ManagerRegistry $registry)
    {
        parent::__construct($registry, Job::class);
    }

    /**
     * @return list<Job>
     */
    public function findPublished(string $query = ''): array
    {
        $qb = $this->createQueryBuilder('j')
            ->andWhere('j.published = :yes')
            ->setParameter('yes', true)
            ->orderBy('j.createdAt', 'DESC');

        if ($query !== '') {
            $qb->andWhere('LOWER(j.title) LIKE :q OR LOWER(j.description) LIKE :q')
                ->setParameter('q', '%'.strtolower($query).'%');
        }

        return $qb->getQuery()->getResult();
    }
}
''',
)

w(
    "src/Service/ApplicationManager.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Service;

use App\Entity\Application;
use App\Entity\Candidate;
use App\Entity\Job;
use Doctrine\ORM\EntityManagerInterface;

/**
 * Synchronous in-process application use-case (teaching monolith coupling point).
 */
final class ApplicationManager
{
    public function __construct(private EntityManagerInterface $em)
    {
    }

    public function apply(Candidate $candidate, Job $job, ?string $letter): Application
    {
        if (!$job->isPublished()) {
            throw new \DomainException('The job is not open.');
        }

        $existing = $this->em->getRepository(Application::class)->findOneBy([
            'candidate' => $candidate,
            'job' => $job,
        ]);

        if ($existing) {
            throw new \DomainException('The candidate has already applied.');
        }

        $application = (new Application())
            ->setCandidate($candidate)
            ->setJob($job)
            ->setCoverLetter($letter);

        $this->em->persist($application);
        $this->em->flush();

        return $application;
    }
}
''',
)

w(
    "src/Kernel.php",
    r'''
<?php

declare(strict_types=1);

namespace App;

use Symfony\Bundle\FrameworkBundle\Kernel\MicroKernelTrait;
use Symfony\Component\HttpKernel\Kernel as BaseKernel;

final class Kernel extends BaseKernel
{
    use MicroKernelTrait;
}
''',
)

w(
    "src/Controller/HomeController.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Job;
use App\Repository\JobRepository;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;

final class HomeController extends AbstractController
{
    #[Route('/', name: 'app_home')]
    public function index(Request $request, JobRepository $jobs): Response
    {
        $q = (string) $request->query->get('q', '');

        return $this->render('home/index.html.twig', [
            'jobs' => $jobs->findPublished($q),
            'q' => $q,
        ]);
    }

    #[Route('/jobs/{id}', name: 'app_job_show', requirements: ['id' => '\\d+'])]
    public function show(Job $job): Response
    {
        return $this->render('home/show.html.twig', [
            'job' => $job,
        ]);
    }
}
''',
)

w(
    "src/Controller/SecurityController.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Authentication\AuthenticationUtils;

final class SecurityController extends AbstractController
{
    #[Route('/login', name: 'app_login')]
    public function login(AuthenticationUtils $authenticationUtils): Response
    {
        return $this->render('security/login.html.twig', [
            'last_username' => $authenticationUtils->getLastUsername(),
            'error' => $authenticationUtils->getLastAuthenticationError(),
        ]);
    }

    #[Route('/logout', name: 'app_logout')]
    public function logout(): never
    {
        throw new \LogicException('Handled by the firewall.');
    }
}
''',
)

w(
    "src/Controller/AdminController.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Application;
use App\Entity\Candidate;
use App\Entity\Company;
use App\Entity\Job;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/admin')]
#[IsGranted('ROLE_ADMIN')]
final class AdminController extends AbstractController
{
    #[Route('', name: 'admin_dashboard')]
    public function index(EntityManagerInterface $em): Response
    {
        return $this->render('admin/index.html.twig', [
            'counts' => [
                'candidates' => $em->getRepository(Candidate::class)->count([]),
                'companies' => $em->getRepository(Company::class)->count([]),
                'jobs' => $em->getRepository(Job::class)->count([]),
                'applications' => $em->getRepository(Application::class)->count([]),
            ],
        ]);
    }
}
''',
)

w(
    "src/Controller/CandidateController.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Application;
use App\Entity\Candidate;
use App\Entity\Job;
use App\Entity\User;
use App\Service\ApplicationManager;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/candidate')]
#[IsGranted('ROLE_CANDIDATE')]
final class CandidateController extends AbstractController
{
    private function candidate(EntityManagerInterface $em): Candidate
    {
        $user = $this->getUser();
        if (!$user instanceof User) {
            throw $this->createAccessDeniedException();
        }

        $candidate = $em->getRepository(Candidate::class)->findOneBy(['user' => $user]);
        if (!$candidate) {
            throw $this->createNotFoundException('Candidate profile not found.');
        }

        return $candidate;
    }

    #[Route('/applications', name: 'candidate_applications')]
    public function applications(EntityManagerInterface $em): Response
    {
        $applications = $em->getRepository(Application::class)->findBy(
            ['candidate' => $this->candidate($em)],
            ['submittedAt' => 'DESC']
        );

        return $this->render('candidate/applications.html.twig', [
            'applications' => $applications,
        ]);
    }

    #[Route('/jobs/{id}/apply', name: 'candidate_apply', methods: ['GET', 'POST'])]
    public function apply(
        Job $job,
        Request $request,
        EntityManagerInterface $em,
        ApplicationManager $manager,
    ): Response {
        if ($request->isMethod('POST')) {
            if (!$this->isCsrfTokenValid('apply'.$job->getId(), (string) $request->request->get('_token'))) {
                throw $this->createAccessDeniedException();
            }

            try {
                $manager->apply(
                    $this->candidate($em),
                    $job,
                    $request->request->get('coverLetter')
                );
                $this->addFlash('success', 'Application submitted.');

                return $this->redirectToRoute('candidate_applications');
            } catch (\DomainException $e) {
                $this->addFlash('danger', $e->getMessage());
            }
        }

        return $this->render('candidate/apply.html.twig', [
            'job' => $job,
        ]);
    }
}
''',
)

w(
    "src/Controller/CompanyController.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Controller;

use App\Entity\Company;
use App\Entity\Job;
use App\Entity\User;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Attribute\Route;
use Symfony\Component\Security\Http\Attribute\IsGranted;

#[Route('/company')]
#[IsGranted('ROLE_COMPANY')]
final class CompanyController extends AbstractController
{
    private function company(EntityManagerInterface $em): Company
    {
        $user = $this->getUser();
        if (!$user instanceof User) {
            throw $this->createAccessDeniedException();
        }

        $company = $em->getRepository(Company::class)->findOneBy(['owner' => $user]);
        if (!$company) {
            throw $this->createNotFoundException();
        }

        return $company;
    }

    #[Route('/jobs', name: 'company_jobs')]
    public function jobs(EntityManagerInterface $em): Response
    {
        $jobs = $em->getRepository(Job::class)->findBy(
            ['company' => $this->company($em)],
            ['createdAt' => 'DESC']
        );

        return $this->render('company/jobs.html.twig', [
            'jobs' => $jobs,
        ]);
    }

    #[Route('/jobs/new', name: 'company_job_new', methods: ['GET', 'POST'])]
    public function new(Request $request, EntityManagerInterface $em): Response
    {
        $job = (new Job())->setCompany($this->company($em));

        if ($request->isMethod('POST')) {
            if (!$this->isCsrfTokenValid('new-job', (string) $request->request->get('_token'))) {
                throw $this->createAccessDeniedException();
            }

            $job
                ->setTitle((string) $request->request->get('title'))
                ->setDescription((string) $request->request->get('description'))
                ->setContractType((string) $request->request->get('contractType', 'CDI'))
                ->setLocation($request->request->get('location'))
                ->setRemote($request->request->getBoolean('remote'))
                ->setPublished($request->request->getBoolean('published'));

            $em->persist($job);
            $em->flush();

            return $this->redirectToRoute('company_jobs');
        }

        return $this->render('company/new.html.twig', [
            'job' => $job,
        ]);
    }
}
''',
)

w(
    "src/DataFixtures/AppFixtures.php",
    r'''
<?php

declare(strict_types=1);

namespace App\DataFixtures;

use App\Entity\Candidate;
use App\Entity\Company;
use App\Entity\Job;
use App\Entity\Skill;
use App\Entity\User;
use Doctrine\Bundle\FixturesBundle\Fixture;
use Doctrine\Persistence\ObjectManager;
use Symfony\Component\PasswordHasher\Hasher\UserPasswordHasherInterface;

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

        $makeUser('admin@jobboard.local', ['ROLE_ADMIN'], 'System', 'Admin');
        $recruiter = $makeUser('recruiter@jobboard.local', ['ROLE_COMPANY'], 'Robin', 'Recruiter');
        $candidateUser = $makeUser('candidate@jobboard.local', ['ROLE_CANDIDATE'], 'Casey', 'Candidate');

        $company = (new Company())
            ->setName('Northstar Digital')
            ->setCity('Tunis')
            ->setDescription('A demonstration employer for the JobBoard teaching project.')
            ->setOwner($recruiter);

        $candidate = (new Candidate())
            ->setUser($candidateUser)
            ->setHeadline('Software Engineering Student')
            ->setSummary('Interested in distributed Web applications.');

        foreach (['PHP', 'Symfony', 'REST', 'MySQL'] as $name) {
            $skill = (new Skill())->setName($name);
            $manager->persist($skill);
            $candidate->addSkill($skill);
        }

        $job = (new Job())
            ->setCompany($company)
            ->setTitle('Junior Symfony Developer')
            ->setDescription('Build and maintain Web features in a collaborative engineering team.')
            ->setContractType('INTERNSHIP')
            ->setLocation('Tunis')
            ->setRemote(true)
            ->setPublished(true);

        $manager->persist($company);
        $manager->persist($candidate);
        $manager->persist($job);
        $manager->flush();
    }
}
''',
)

w(
    "tests/Controller/HomeControllerTest.php",
    r'''
<?php

declare(strict_types=1);

namespace App\Tests\Controller;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

final class HomeControllerTest extends WebTestCase
{
    public function testHomePageLoads(): void
    {
        $client = static::createClient();
        $client->request('GET', '/');

        self::assertResponseIsSuccessful();
        self::assertSelectorTextContains('.brand', 'JobBoard');
    }
}
''',
)

w(
    "bin/console",
    r'''
#!/usr/bin/env php
<?php

use App\Kernel;
use Symfony\Bundle\FrameworkBundle\Console\Application;

if (!is_dir(dirname(__DIR__).'/vendor')) {
    throw new LogicException('Dependencies are missing. Run composer install.');
}

require_once dirname(__DIR__).'/vendor/autoload_runtime.php';

return function (array $context) {
    $kernel = new Kernel($context['APP_ENV'], (bool) $context['APP_DEBUG']);

    return new Application($kernel);
};
''',
)

# --- Twig ---
w(
    "templates/base.html.twig",
    r'''
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{% block title %}JobBoard{% endblock %}</title>
    <link rel="stylesheet" href="{{ asset('css/app.css') }}">
</head>
<body>
<header>
    <a class="brand" href="{{ path('app_home') }}">JobBoard</a>
    <nav>
        <a href="{{ path('app_home') }}">Jobs</a>
        {% if is_granted('ROLE_CANDIDATE') %}
            <a href="{{ path('candidate_applications') }}">My applications</a>
        {% endif %}
        {% if is_granted('ROLE_COMPANY') %}
            <a href="{{ path('company_jobs') }}">Company jobs</a>
        {% endif %}
        {% if is_granted('ROLE_ADMIN') %}
            <a href="{{ path('admin_dashboard') }}">Admin</a>
        {% endif %}
        {% if app.user %}
            <a href="{{ path('app_logout') }}">Logout</a>
        {% else %}
            <a href="{{ path('app_login') }}">Login</a>
        {% endif %}
    </nav>
</header>

{% for type, messages in app.flashes %}
    {% for message in messages %}
        <div class="flash {{ type }}">{{ message }}</div>
    {% endfor %}
{% endfor %}

<main>
    {% block body %}{% endblock %}
</main>

<footer>ESPRIT · Distributed Web Applications · Teaching monolith</footer>
</body>
</html>
''',
)

w(
    "templates/home/index.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Jobs · JobBoard{% endblock %}

{% block body %}
<section class="hero">
    <h1>Find your next opportunity</h1>
    <form>
        <input name="q" value="{{ q }}" placeholder="Search jobs">
        <button>Search</button>
    </form>
</section>

<section class="cards">
    {% for job in jobs %}
        <article>
            <h2><a href="{{ path('app_job_show', {id: job.id}) }}">{{ job.title }}</a></h2>
            <p>{{ job.company.name }} · {{ job.location ?: 'Location flexible' }}</p>
            <span>{{ job.contractType }}</span>
            {% if job.remote %}<span>Remote</span>{% endif %}
        </article>
    {% else %}
        <p>No published jobs found.</p>
    {% endfor %}
</section>
{% endblock %}
''',
)

w(
    "templates/home/show.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}{{ job.title }}{% endblock %}

{% block body %}
<article class="detail">
    <h1>{{ job.title }}</h1>
    <p><b>{{ job.company.name }}</b> · {{ job.location }}</p>
    <p>{{ job.description }}</p>
    {% if is_granted('ROLE_CANDIDATE') %}
        <a class="button" href="{{ path('candidate_apply', {id: job.id}) }}">Apply</a>
    {% endif %}
</article>
{% endblock %}
''',
)

w(
    "templates/security/login.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Login · JobBoard{% endblock %}

{% block body %}
<form class="panel" method="post">
    <h1>Login</h1>
    {% if error %}
        <div class="flash danger">{{ error.messageKey|trans(error.messageData, 'security') }}</div>
    {% endif %}
    <label>Email
        <input name="email" type="email" value="{{ last_username }}" required>
    </label>
    <label>Password
        <input name="password" type="password" required>
    </label>
    <input type="hidden" name="_csrf_token" value="{{ csrf_token('authenticate') }}">
    <button>Login</button>
    <p>Demo passwords: <code>password</code></p>
</form>
{% endblock %}
''',
)

w(
    "templates/candidate/apply.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Apply · JobBoard{% endblock %}

{% block body %}
<form class="panel" method="post">
    <h1>Apply for {{ job.title }}</h1>
    <label>Cover letter
        <textarea name="coverLetter" rows="9"></textarea>
    </label>
    <input type="hidden" name="_token" value="{{ csrf_token('apply' ~ job.id) }}">
    <button>Submit application</button>
</form>
{% endblock %}
''',
)

w(
    "templates/candidate/applications.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}My applications · JobBoard{% endblock %}

{% block body %}
<h1>My applications</h1>
<section class="cards">
    {% for a in applications %}
        <article>
            <h2>{{ a.job.title }}</h2>
            <p>{{ a.job.company.name }}</p>
            <span>{{ a.status }}</span>
            <small>{{ a.submittedAt|date('Y-m-d H:i') }}</small>
        </article>
    {% else %}
        <p>No applications yet.</p>
    {% endfor %}
</section>
{% endblock %}
''',
)

w(
    "templates/company/jobs.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Company jobs · JobBoard{% endblock %}

{% block body %}
<h1>Company jobs</h1>
<a class="button" href="{{ path('company_job_new') }}">Create a job</a>
<section class="cards">
    {% for job in jobs %}
        <article>
            <h2>{{ job.title }}</h2>
            <p>{{ job.contractType }} · {{ job.published ? 'Published' : 'Draft' }}</p>
            <b>{{ job.applications|length }} application(s)</b>
        </article>
    {% endfor %}
</section>
{% endblock %}
''',
)

w(
    "templates/company/new.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Create job · JobBoard{% endblock %}

{% block body %}
<form class="panel" method="post">
    <h1>Create a job</h1>
    <label>Title
        <input name="title" required>
    </label>
    <label>Description
        <textarea name="description" rows="8" required></textarea>
    </label>
    <label>Contract
        <select name="contractType">
            <option>CDI</option>
            <option>CDD</option>
            <option>INTERNSHIP</option>
            <option>FREELANCE</option>
        </select>
    </label>
    <label>Location
        <input name="location">
    </label>
    <label><input type="checkbox" name="remote" value="1"> Remote</label>
    <label><input type="checkbox" name="published" value="1"> Publish now</label>
    <input type="hidden" name="_token" value="{{ csrf_token('new-job') }}">
    <button>Create</button>
</form>
{% endblock %}
''',
)

w(
    "templates/admin/index.html.twig",
    r'''
{% extends 'base.html.twig' %}

{% block title %}Admin · JobBoard{% endblock %}

{% block body %}
<h1>Administration dashboard</h1>
<section class="stats">
    {% for label, value in counts %}
        <article>
            <b>{{ value }}</b>
            <span>{{ label|capitalize }}</span>
        </article>
    {% endfor %}
</section>
{% endblock %}
''',
)

w(
    "public/css/app.css",
    r'''
:root {
    --r: #a61c2a;
    --n: #1f3864;
    --bg: #f4f6f9;
    --ink: #20242a;
}

* { box-sizing: border-box; }

body {
    margin: 0;
    background: var(--bg);
    color: var(--ink);
    font: 16px/1.55 system-ui, sans-serif;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 6vw;
    background: #fff;
    box-shadow: 0 2px 10px #0001;
}

.brand {
    font-size: 24px;
    font-weight: 900;
    color: var(--r);
    text-decoration: none;
}

nav a {
    margin-left: 18px;
    color: var(--n);
    font-weight: 700;
    text-decoration: none;
}

main {
    width: min(1100px, 90vw);
    margin: 34px auto;
}

.hero {
    background: linear-gradient(120deg, var(--n), #365d99);
    color: #fff;
    padding: 36px;
    border-radius: 16px;
}

.hero form {
    display: flex;
    gap: 10px;
}

.hero input { flex: 1; }

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 16px;
    margin-top: 22px;
}

.cards article,
.panel,
.detail,
.stats article {
    background: #fff;
    border: 1px solid #d9dee7;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 8px 20px #1f386412;
}

.cards a { color: var(--n); }

span {
    display: inline-block;
    background: #eef3fa;
    color: var(--n);
    padding: 4px 8px;
    border-radius: 20px;
    margin: 3px;
}

input,
textarea,
select {
    width: 100%;
    padding: 11px;
    margin: 5px 0 14px;
    border: 1px solid #aeb7c5;
    border-radius: 8px;
}

input[type=checkbox] { width: auto; }

button,
.button {
    display: inline-block;
    border: 0;
    background: var(--r);
    color: #fff;
    padding: 10px 16px;
    border-radius: 8px;
    text-decoration: none;
    font-weight: 800;
}

.panel {
    max-width: 620px;
    margin: auto;
}

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
}

.stats b {
    display: block;
    color: var(--r);
    font-size: 36px;
}

.flash {
    margin: 16px auto;
    padding: 12px 18px;
    width: min(900px, 90vw);
    background: #e9f7f0;
}

.danger { background: #fbeaec; }

footer {
    text-align: center;
    color: #667085;
    padding: 30px;
}

@media (max-width: 650px) {
    .stats { grid-template-columns: 1fr; }
    .hero form { display: block; }
}
''',
)

print("done")
