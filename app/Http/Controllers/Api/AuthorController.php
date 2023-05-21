<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use Illuminate\Http\Request;
use App\Models\Authors;

class AuthorController extends BaseController
{
    /**
     * get all authors
     * 
     * @return \Illuminate\Http\Response
     */
    public function getAuthors() {
        // get unique authors
        $authors = Authors::select('name', 'id')->distinct()->get();
        
        return $this->sendResponse($authors->toArray(), 'Authors retrieved successfully.');
    }
}
