<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController;

class SourceController extends BaseController
{
    public function getSources() {
        return $this->sendResponse([
            [
                'id' => 'nytimes',
                'label' => 'New York Times',
            ],
        ], 'Sources retrieved successfully.');
    }
}
