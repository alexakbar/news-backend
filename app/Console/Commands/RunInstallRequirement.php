<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

class RunInstallRequirement extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'python:install-requirement';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Command For Install Requirement Python';

    /**
     * Execute the console command.
     */
    public function handle()
    {
        // install requirements.txt
        $process = new Process(['pip3','install','-r','app/Collections/requirements.txt']);
        $process->run();

        // executes after the command finishes
        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $output = $process->getOutput();
        $this->info($output);
    }
}
