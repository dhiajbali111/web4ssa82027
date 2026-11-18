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
    private function candidate(EntityManagerInterface $em): ?Candidate
    {
        $user = $this->getUser();
        if (!$user instanceof User) {
            throw $this->createAccessDeniedException();
        }

        return $em->getRepository(Candidate::class)->findOneBy(['user' => $user]);
    }

    #[Route('/applications', name: 'candidate_applications')]
    public function applications(EntityManagerInterface $em): Response
    {
        $candidate = $this->candidate($em);
        if (!$candidate) {
            $this->addFlash('danger', 'No candidate profile for this account. Log in as candidate@jobboard.local.');

            return $this->redirectToRoute('app_home');
        }

        $applications = $em->getRepository(Application::class)->findBy(
            ['candidate' => $candidate],
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
        $candidate = $this->candidate($em);
        if (!$candidate) {
            $this->addFlash('danger', 'No candidate profile for this account. Log in as candidate@jobboard.local.');

            return $this->redirectToRoute('app_home');
        }

        if ($request->isMethod('POST')) {
            if (!$this->isCsrfTokenValid('apply'.$job->getId(), (string) $request->request->get('_token'))) {
                throw $this->createAccessDeniedException();
            }

            try {
                $manager->apply(
                    $candidate,
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
