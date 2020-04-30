package controllers

import com.fasterxml.jackson.databind.ObjectMapper
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory
import helpers.Html
import io.ktor.application.ApplicationCall
import io.ktor.http.ContentType
import io.ktor.response.respondText
import libs.json.Node
import libs.json.toJson
import java.io.File
import java.nio.file.Paths

class Resume (val call: ApplicationCall){
    suspend fun short(){
        val lang = call.parameters["lang"]!!
        val n = readYaml()

        val experience = n["companies"].toListNotNull { (_,v)->
            mapOf(
                    "name" to v["name"][lang].toString,
                    "position" to v["position"][lang].toString,
                    "description" to v["description"][lang].toList().joinToString() ,
                    "duration" to v["duration"].toString
            )
        }

        val programs = n["programs"].toListNotNull { (_,v)->
            mapOf(
                    "name" to v["name"].toString,
                    "lastuse" to v["lastuse"].toString,
                    "level" to v["level"].toString
            )
        }

        val attainments = n["attainments"]["items"].toListNotNull {(_,v)->
            mapOf(
                    "keywords"  to v["keywords"].toListNotNull { (_,k)->k.toString }.joinToString(", "),
                    "description"  to v["description"][lang].toListNotNull { (_,k)->k.toString }.joinToString("<br>"),
                    "summary" to v["summary"][lang].toString,
                    "company" to v["company"][lang].toString,
                    "display" to v["display"].toString
            )
        }.filter { it["display"]=="true" }


        val html = Html("/short.ftl").render(
                "name_zh" to n["name"]["zh"].toString,
                "name_en" to n["name"]["en"].toString,
                "phones" to n["phones"][0].toString,//.toListNotNull { (_,v)-> v.toString }.joinToString("<br>"),
                "mail" to n["mail"].toString,
                "github" to n["github"].toString,
                "profile" to n["profile"]["zh"].toListNotNull { (_,v)-> v.toString }.joinToString("<br>"),

                "libraries" to n["libraries"].toListNotNull { (_,v)-> v.toString }.joinToString(", "),
                "databases" to n["databases"].toListNotNull { (_,v)-> v.toString }.joinToString(", "),
                "vc" to n["vsersion controlls"].toListNotNull { (_,v)-> v.toString }.joinToString(", "),
                "os" to n["os"].toListNotNull { (_,v)-> v.toString }.joinToString(", "),
                "knowledge" to n["special experiences and knowledge"].toListNotNull { (_,v)-> v.toString }.joinToString(", "),

                "attainments" to attainments,
                "blog" to n["blog"].toString,
                "experience" to experience,
                "programs" to programs,
                "licenses" to n["licenses"].toListNotNull { (_,v)-> v["name"].toString }
        )

        call.respondText(html, ContentType.Text.Html)
    }

    suspend fun full(){

    }

    private fun readYaml():Node{
        val content = File("resume.yaml").readText()
        val jsonNode = ObjectMapper( YAMLFactory() ).readTree(content)
        val writer = ObjectMapper()
        val jsonStr = writer.writeValueAsString(jsonNode)
        return Node.ofMap(jsonStr)
    }

}