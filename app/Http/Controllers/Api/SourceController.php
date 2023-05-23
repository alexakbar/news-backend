<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController;

class SourceController extends BaseController
{
    public function getSources() {
        return $this->sendResponse([
            [
                'id' => 'nytimes',
                'name' => 'New York Times',
            ],
            [
                'id' => 'newsapi',
                'name' => 'News API',
            ],
            [
                'id' => 'theguardian',
                'name' => 'The Guardian',
            ]
        ], 'Sources retrieved successfully.');
    }
}
