<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use App\Models\Category;

class CategoryController extends BaseController
{
    /**
     * get all categories
     * 
     * @return \Illuminate\Http\Response
     */
    public function getCategories() {
        // get unique categories
        $categories = Category::select('name', 'id')->distinct()->get();

        return $this->sendResponse($categories->toArray(), 'Categories retrieved successfully.');
    }
}
