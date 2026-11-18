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
