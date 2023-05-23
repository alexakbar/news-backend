<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Api\BaseController as BaseController;
use App\Models\News;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use jcobhams\NewsApi\NewsApi;

class ArticlesController extends BaseController
{

    /**
     * search articles
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function searchArticles(Request $request): JsonResponse
    {
        // get search keyword
        $query = $request->q;
        // get filter inputs
        $filterCategories = $request->categories;
        $filterStartDate = $request->start_date;
        $filterEndDate = $request->end_date;
        $filterSources = $request->sources;

        $posts = News::query();

        // serach by keyword
        if ($query) {
            $posts->where(function ($q) use ($query) {
                $q->where('title', 'LIKE', "%$query%")
                    ->orWhere('description', 'LIKE', "%$query%");
            });
        }

        // filter categories
        if ($filterCategories) {
            $posts->whereIn('category', $filterCategories);
        }

        // filter start date
        if ($filterStartDate) {
            $posts->whereDate('published_at', '>=', $filterStartDate);
        }

        // filter end date
        if ($filterEndDate) {
            $posts->whereDate('published_at', '<=', $filterEndDate);
        }

        // filter prefred sources
        if ($filterSources) {
            $posts->whereIn('source', $filterSources);
        }

        $results = $posts->get();

        return $this->sendResponse($results->toArray(), 'Articles retrieved successfully.');
    }
}
