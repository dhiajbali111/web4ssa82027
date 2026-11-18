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
    private function company(EntityManagerInterface $em): ?Company
    {
        $user = $this->getUser();
        if (!$user instanceof User) {
            throw $this->createAccessDeniedException();
        }

        return $em->getRepository(Company::class)->findOneBy(['owner' => $user]);
    }

    #[Route('/jobs', name: 'company_jobs')]
    public function jobs(EntityManagerInterface $em): Response
    {
        $company = $this->company($em);
        if (!$company) {
            $this->addFlash('danger', 'No company profile for this account. Log in as recruiter@jobboard.local.');

            return $this->redirectToRoute('app_home');
        }

        $jobs = $em->getRepository(Job::class)->findBy(
            ['company' => $company],
            ['createdAt' => 'DESC']
        );

        return $this->render('company/jobs.html.twig', [
            'jobs' => $jobs,
        ]);
    }

    #[Route('/jobs/new', name: 'company_job_new', methods: ['GET', 'POST'])]
    public function new(Request $request, EntityManagerInterface $em): Response
    {
        $company = $this->company($em);
        if (!$company) {
            $this->addFlash('danger', 'No company profile for this account. Log in as recruiter@jobboard.local.');

            return $this->redirectToRoute('app_home');
        }

        $job = (new Job())->setCompany($company);

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
