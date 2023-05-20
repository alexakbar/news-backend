<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use Illuminate\Http\JsonResponse;
use Illuminate\Support\Facades\Auth;

class UserController extends BaseController
{
    /**
     * get user
     * 
     * @return \Illuminate\Http\JsonResponse
     */
    public function getUser(): JsonResponse
    {
        // get user 
        $user = Auth::user();
        return $this->sendResponse($user, 'User retrieved successfully.');
    }
}
